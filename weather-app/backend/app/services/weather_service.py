from sqlalchemy.orm import Session
from sqlalchemy import desc

from ..models import Measurement


def get_latest_measurement(
    db: Session,
    metric: str
):
    return (
        db.query(Measurement)
        .filter(Measurement.metric == metric)
        .order_by(desc(Measurement.recorded_at))
        .first()
    )


def get_measurements_history(
    db: Session,
    metric: str,
    limit: int = 20
):
    return (
        db.query(Measurement)
        .filter(Measurement.metric == metric)
        .order_by(desc(Measurement.recorded_at))
        .limit(limit)
        .all()
    )