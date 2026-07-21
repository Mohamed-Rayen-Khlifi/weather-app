from datetime import datetime
from pydantic import BaseModel


class MeasurementResponse(BaseModel):

    metric: str

    value: float

    recorded_at: datetime

    class Config:

        from_attributes = True


class ForecastResponse(BaseModel):

    metric: str

    forecast: float

    based_on: int

    last_values: list[float]


class HealthResponse(BaseModel):

    status: str

    service: str

    time: datetime