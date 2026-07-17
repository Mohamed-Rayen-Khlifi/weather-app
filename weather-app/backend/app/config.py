import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:admin123@localhost:5432/weather_db")
    OPENMETEO_URL = "https://api.open-meteo.com/v1/forecast"
    CITY_LAT = 36.8065  
    CITY_LON = 10.1815
    SECRET_key=os.getenv("SECRET_key","ma_clef_secrete_123456")
    DEBUG=True
    FORECAST_DAYS=7