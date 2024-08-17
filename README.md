# python-tech-test
This is a FastAPI application that collects and stores weather data for a list of city IDs using the OpenWeatherMap API. The application can be run locally or inside a Docker container.

## Features
Collect weather data for a list of city IDs.
Store the weather data in a SQLite database.
Deploy the application using Docker.
Use environment variables with python-dotenv.

## Prerequisites
Create an account at  Open Weather API
Before running the application, ensure you have the following installed:
Python 3.9 or higher (for local development)
Docker (for containerization)

## Setup
1. Clone the Repository
  git clone <repository_url>
  cd <repository_directory>
  
2. Set Up Environment Variables
   API_KEY=your_openweathermap_api_key

## Dockerization
You can run the application inside a Docker container, which eliminates the need for setting up a virtual environment locally.

1. Build the Docker Image
   docker build -t my-fastapi-app .

2. Run the Docker Container
   docker run -d -p 8000:8000 my-fastapi-app
   
The application will be accessible at http://localhost:8000.

3. Access API Documentation
   FastAPI provides interactive API documentation:
   Swagger UI: http://localhost:8000/docs

## Database
The weather data is stored in a SQLite database (weather.db). To inspect the data:
