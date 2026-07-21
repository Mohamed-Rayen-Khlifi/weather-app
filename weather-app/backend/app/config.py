import os
from dotenv import load_dotenv

load_dotenv()


class Config:

    # Database
    # SQLite temporaire pour le développement
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "sqlite:///./weather.db"
    )


    # Open Meteo API
    OPENMETEO_URL = (
        "https://api.open-meteo.com/v1/forecast"
    )


    # Location (Tunis)
    CITY_LAT = float(
        os.getenv(
            "CITY_LAT",
            36.8065
        )
    )

    CITY_LON = float(
        os.getenv(
            "CITY_LON",
            10.1815
        )
    )


    # Security
    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "ma_clef_secrete_123456"
    )


    # Application
    DEBUG = os.getenv(
        "DEBUG",
        "False"
    ).lower() == "true"


    # Forecast
    FORECAST_DAYS = int(
        os.getenv(
            "FORECAST_DAYS",
            7
        )
    )