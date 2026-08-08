from sqlalchemy.orm import Session
from sklearn.ensemble import IsolationForest
import numpy as np

from ..models import Measurement


def detect_anomalies(db: Session, metric: str):

    records = (
        db.query(Measurement)
        .filter(Measurement.metric == metric)
        .order_by(Measurement.recorded_at.asc())
        .all()
    )

    print("AI ANOMALY")
    print("Metric:", metric)
    print("Records:", len(records))

    if len(records) < 10:
        return {
            "metric": metric,
            "total_records": len(records),
            "anomalies_count": 0,
            "anomalies": [],
            "message": "Not enough data"
        }

    values = np.array([[record.value] for record in records])

    model = IsolationForest(
        contamination=0.1,
        random_state=42
    )

    model.fit(values)

    predictions = model.predict(values)
    scores = model.decision_function(values)

    anomalies = []

    for record, prediction, score in zip(
        records,
        predictions,
        scores
    ):

        if prediction == -1:

            anomalies.append({
                "id": record.id,
                "metric": record.metric,
                "value": record.value,
                "recorded_at": str(record.recorded_at),
                "anomaly_score": round(float(score), 4)
            })

    return {
        "metric": metric,
        "total_records": len(records),
        "anomalies_count": len(anomalies),
        "anomalies": anomalies,
        "model": "Isolation Forest"
    }