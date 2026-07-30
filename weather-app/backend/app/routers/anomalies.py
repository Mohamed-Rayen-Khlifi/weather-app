from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..services.anomaly_service import get_anomalies
from ..schemas import AnomalyRequest


router = APIRouter(
    tags=["Anomalies"]
)



@router.put("/anomalies")
def anomalies(
    request: AnomalyRequest,
    db: Session = Depends(get_db)
):

    return get_anomalies(
        db=db,
        metric=request.metric,
        threshold=request.threshold
    )