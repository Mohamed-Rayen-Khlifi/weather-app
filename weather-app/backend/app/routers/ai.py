from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..ai.predictor import predict_weather
from ..schemas import ForecastRequest


router = APIRouter(
    tags=["AI"]
)



@router.put("/ai/predict")
def ai_predict(
    request: ForecastRequest,
    db: Session = Depends(get_db)
):

    return predict_weather(
        db=db,
        metric=request.metric
    )