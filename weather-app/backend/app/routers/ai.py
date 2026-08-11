from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..ai.predictor import predict_weather
from ..ai.anomaly_ai import detect_anomalies
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


@router.get("/ai/anomalies/{metric}")
def ai_anomalies(
    metric: str,
    db: Session = Depends(get_db)
):
    return detect_anomalies(
        db=db,
        metric=metric
    )