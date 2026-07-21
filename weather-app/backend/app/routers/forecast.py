
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..services.forecast_service import get_forecast

router = APIRouter(tags=["Forecast"])


@router.get("/forecast")
def forecast(
    db: Session = Depends(get_db),
):
    return get_forecast(db)