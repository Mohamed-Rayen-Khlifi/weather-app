 import requests
from sqlalchemy.orm import Session
from .models import Measurement, CollectorLog
from .config import Config
from datetime import datetime

def fetch_weather():
    params = {
        "latitude": Config.CITY_LAT,
        "longitude": Config.CITY_LON,
        "current_weather": True,
        "hourly": "temperature_2m,relativehumidity_2m,windspeed_10m,pressure_msl"
    }
    
    response = requests.get(Config.OPENMETEO_URL, params=params)
    response.raise_for_status()
    data = response.json()
    
    hourly = data.get("hourly", {})
    if not hourly:
        return None
    
    idx = -1
    return {
        "temperature": hourly["temperature_2m"][idx],
        "humidity": hourly["relativehumidity_2m"][idx],
        "windspeed": hourly["windspeed_10m"][idx],
        "pressure": hourly["pressure_msl"][idx],
        "recorded_at": datetime.utcnow()
    }

def save_weather(db: Session):
    log = CollectorLog(status="running", rows_saved=0)
    
    try:
        data = fetch_weather()
        if not data:
            log.status = "error"
            log.message = "No data from API"
            db.add(log)
            db.commit()
            return
        
        metrics = [
            ("temperature", data["temperature"]),
            ("humidity", data["humidity"]),
            ("windspeed", data["windspeed"]),
            ("pressure", data["pressure"])
        ]
        
        for metric, value in metrics:
            measurement = Measurement(
                source="open-meteo",
                metric=metric,
                value=value,
                recorded_at=data["recorded_at"]
            )
            db.add(measurement)
        
        log.status = "success"
        log.rows_saved = len(metrics)
        log.message = f"Saved {len(metrics)} metrics at {data['recorded_at']}"
        
    except Exception as e:
        log.status = "error"
        log.message = str(e)
    
    db.add(log)
    db.commit()