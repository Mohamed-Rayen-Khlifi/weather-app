from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..services.weather_service import (
    get_latest_measurement,
    get_measurements_history,
)

router = APIRouter(tags=["Weather"])


@router.get("/measurements/latest")
def latest_measurement(
    metric: str = Query(...),
    db: Session = Depends(get_db),
):
    measurement = get_latest_measurement(
        db=db,
        metric=metric,
    )

    if measurement is None:
        return {
            "message": "No data found"
        }

    return {
        "id": measurement.id,
        "metric": measurement.metric,
        "value": measurement.value,
        "recorded_at": measurement.recorded_at,
    }


@router.get("/measurements")
def measurements_history(
    metric: str = Query(...),
    limit: int = Query(20),
    db: Session = Depends(get_db),
):
    measurements = get_measurements_history(
        db=db,
        metric=metric,
        limit=limit,
    )

    return [
        {
            "id": item.id,
            "metric": item.metric,
            "value": item.value,
            "recorded_at": item.recorded_at,
        }
        for item in measurements
    ]