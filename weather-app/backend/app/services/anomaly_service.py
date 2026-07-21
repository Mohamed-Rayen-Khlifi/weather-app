from sqlalchemy.orm import Session
from sqlalchemy import desc
import pandas as pd

from ..models import Measurement


def get_anomalies(
    db: Session,
    metric: str = "temperature",
    threshold: float = 3.0
):

    records = (
        db.query(Measurement)
        .filter(Measurement.metric == metric)
        .order_by(desc(Measurement.recorded_at))
        .limit(50)
        .all()
    )

    if len(records) < 10:
        return {
            "anomalies": [],
            "message": "Not enough data"
        }

    df = pd.DataFrame([
        {
            "value": r.value,
            "recorded_at": r.recorded_at
        }
        for r in records
    ])

    mean = df["value"].mean()
    std = df["value"].std()

    anomalies = []

    for _, row in df.iterrows():

        z_score = (row["value"] - mean) / std

        if abs(z_score) > threshold:

            anomalies.append({
                "value": row["value"],
                "recorded_at": row["recorded_at"].isoformat(),
                "z_score": round(z_score, 2)
            })

    return {
        "metric": metric,
        "threshold": threshold,
        "mean": round(mean, 2),
        "std": round(std, 2),
        "anomalies": anomalies[-10:]
    }