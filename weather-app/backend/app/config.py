import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:admin123@localhost:5432/weather_db")
    OPENMETEO_URL = "https://api.open-meteo.com/v1/forecast"
    CITY_LAT = 36.8065  # Tunis
    CITY_LON = 10.1815