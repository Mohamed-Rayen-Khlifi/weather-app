from sqlalchemy.orm import Session
from sqlalchemy import desc

from ..models import Measurement


def get_forecast(
    db: Session,
    metric: str = "temperature",
    n_points: int = 5
):

    records = (
        db.query(Measurement)
        .filter(Measurement.metric == metric)
        .order_by(desc(Measurement.recorded_at))
        .limit(n_points)
        .all()
    )


    if len(records) < 2:
        return {
            "metric": metric,
            "forecast": None,
            "message": "Not enough data"
        }


    values = [
        record.value
        for record in reversed(records)
    ]


    # Simple moving average prediction
    forecast = sum(values) / len(values)


    last_measurement = records[0]


    return {

        "metric": metric,

        "forecast": round(forecast, 2),

        "unit": get_unit(metric),

        "based_on": len(values),

        "last_values": values,

        "last_update": last_measurement.recorded_at.isoformat()

    }



def get_unit(metric):

    units = {

        "temperature": "°C",

        "humidity": "%",

        "windspeed": "km/h",

        "pressure": "hPa"

    }


    return units.get(metric, "")