from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..services.weather_service import get_latest_measurement

router = APIRouter(tags=["Dashboard"])


@router.get("/dashboard")
def dashboard_data(
    db: Session = Depends(get_db),
):

    metrics = [
        "temperature",
        "humidity",
        "windspeed",
        "pressure",
    ]

    result = {}

    for metric in metrics:

        measurement = get_latest_measurement(
            db=db,
            metric=metric,
        )

        if measurement:

            result[metric] = {
                "id": measurement.id,
                "metric": measurement.metric,
                "value": measurement.value,
                "recorded_at": measurement.recorded_at,
            }

        else:

            result[metric] = None

    return result