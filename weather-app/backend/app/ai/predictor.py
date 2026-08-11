from sqlalchemy.orm import Session
from sklearn.linear_model import LinearRegression
import numpy as np

from ..models import Measurement



def predict_weather(
    db: Session,
    metric: str,
    future_step: int = 1
):


    records = (
        db.query(Measurement)
        .filter(
            Measurement.metric == metric
        )
        .order_by(
            Measurement.recorded_at.asc()
        )
        .all()
    )



    if len(records) < 5:

        return {

            "metric": metric,

            "prediction": None,

            "message": "Not enough data"

        }



    values = np.array(
        [
            r.value
            for r in records
        ]
    )



    X = np.arange(
        len(values)
    ).reshape(-1,1)


    y = values



    model = LinearRegression()


    model.fit(
        X,
        y
    )



    next_point = np.array(

        [
            [
                len(values)
                +
                future_step
            ]
        ]

    )



    prediction = model.predict(
        next_point
    )[0]



    return {

        "metric": metric,

        "prediction":
            round(float(prediction),2),

        "model":
            "Linear Regression",

        "trained_on":
            len(values)

    }