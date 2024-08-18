from fastapi import FastAPI, HTTPException, Depends
import httpx
import datetime
import asyncio
from sqlalchemy.orm import Session
from models import WeatherData, engine, SessionLocal, database
from time import time
from dotenv import load_dotenv
import os

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.post("/collect-weather/")
async def collect_weather(user_id: str, city_ids: list[int], db: Session = Depends(get_db)):
    global requests_made, request_reset_time

    existing_entries = db.query(WeatherData).filter(WeatherData.user_id == user_id).first()
    if existing_entries:
        raise HTTPException(status_code=400, detail="Weather data for this user ID already exists.")

    weather_data_list = []
    chunk_size = 60  
    city_id_chunks = [city_ids[i:i + chunk_size] for i in range(0, len(city_ids), chunk_size)]
    requests_made = 0
    request_reset_time = time() 

    async with httpx.AsyncClient() as client:
        for chunk in city_id_chunks:
            for city_id in chunk:
                params = {
                    "id": city_id,
                    "appid": API_KEY
                }
                response = await client.get(BASE_URL, params=params)
                response.raise_for_status()
                weather_data = response.json()

                temperature_celsius = round(weather_data["main"].get("temp", 0) - 273.15, 2)

                extracted_data = {
                    "city_id": weather_data.get("id"),
                    "temperature_celsius": temperature_celsius,
                    "humidity": weather_data["main"].get("humidity")
                }

                weather_data_list.append(extracted_data)

                requests_made += 1

            await asyncio.sleep(60)
            requests_made = 0

    for weather_data in weather_data_list:
        db_entry = WeatherData(
            user_id=user_id,
            datetime=datetime.datetime.now(),
            data=weather_data
        )
        db.add(db_entry)
    db.commit()

    return {"message": "Weather data collected successfully."}

@app.get("/progress/{user_id}")
def get_progress(user_id: str, db: Session = Depends(get_db)):

    db_entries = db.query(WeatherData).filter(WeatherData.user_id == user_id).all()
    if not db_entries:
        raise HTTPException(status_code=404, detail="User ID not found.")

    collected_cities = len(db_entries)

    return {"collected_cities": collected_cities, "entries": [entry.data for entry in db_entries]}
