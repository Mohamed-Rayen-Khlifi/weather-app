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

    result = get_latest_measurement(
        db,
        metric
    )

    if result is None:
        return None

    return {
        "id": result.id,
        "metric": result.metric,
        "value": result.value,
        "recorded_at": result.recorded_at,
    }


@router.get("/measurements")
def measurements_history(
    metric: str = Query(...),
    limit: int = Query(20),
    db: Session = Depends(get_db),
):

    results = get_measurements_history(
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
        for item in results
    ]