from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..services.forecast_service import get_forecast
from ..schemas import ForecastRequest


router = APIRouter(tags=["Forecast"])



@router.put("/forecast")
def forecast(
    request: ForecastRequest,
    db: Session = Depends(get_db),
):

    return get_forecast(
        db=db,
        metric=request.metric
    )