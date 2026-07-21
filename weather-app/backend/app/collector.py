import requests
from datetime import datetime
from sqlalchemy.orm import Session

from .models import Measurement, CollectorLog
from .config import Config


def fetch_weather():

    params = {
        "latitude": Config.CITY_LAT,
        "longitude": Config.CITY_LON,
        "current": [
            "temperature_2m",
            "relative_humidity_2m",
            "wind_speed_10m",
            "pressure_msl"
        ]
    }

    try:

        response = requests.get(
            Config.OPENMETEO_URL,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        current = data.get("current")

        if current is None:
            return None

        return {
            "temperature": current.get("temperature_2m"),
            "humidity": current.get("relative_humidity_2m"),
            "windspeed": current.get("wind_speed_10m"),
            "pressure": current.get("pressure_msl"),
            "recorded_at": datetime.utcnow()
        }


    except Exception as e:

        print(f"Weather API Error: {e}")
        return None



def save_weather(db: Session):

    log = CollectorLog(
        status="running",
        rows_saved=0
    )


    try:

        data = fetch_weather()


        if data is None:

            log.status = "error"
            log.message = "No data received from Open-Meteo API"

            db.add(log)
            db.commit()

            return


        metrics = [
            ("temperature", data["temperature"]),
            ("humidity", data["humidity"]),
            ("windspeed", data["windspeed"]),
            ("pressure", data["pressure"])
        ]


        saved_count = 0


        for metric, value in metrics:

            if value is None:
                continue


            measurement = Measurement(
                source="open-meteo",
                metric=metric,
                value=float(value),
                recorded_at=data["recorded_at"]
            )

            db.add(measurement)
            saved_count += 1



        log.status = "success"
        log.rows_saved = saved_count
        log.message = f"Successfully saved {saved_count} measurements"


        db.add(log)

        db.commit()


        print(f"{saved_count} measurements saved successfully")



    except Exception as e:

        db.rollback()

        log.status = "error"
        log.rows_saved = 0
        log.message = str(e)

        db.add(log)
        db.commit()

        print(f"Collector Error: {e}")