from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..services.anomaly_service import get_anomalies

router = APIRouter(tags=["Anomalies"])


@router.get("/anomalies")
def anomalies(
    db: Session = Depends(get_db),
):
    return get_anomalies(db)