from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Index
from sqlalchemy.sql import func
from .database import Base


class Measurement(Base):
    __tablename__ = "measurements"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String(50), default="open-meteo", nullable=False)
    metric = Column(String(50), index=True, nullable=False)
    value = Column(Float, nullable=False)
    recorded_at = Column(DateTime, server_default=func.now(), index=True)

    def __repr__(self):
        return f"<Measurement(metric='{self.metric}', value={self.value}, recorded_at={self.recorded_at})>"


class CollectorLog(Base):
    __tablename__ = "collector_logs"

    id = Column(Integer, primary_key=True, index=True)
    run_at = Column(DateTime, server_default=func.now(), index=True)
    status = Column(String(20), nullable=False)
    rows_saved = Column(Integer, default=0)
    message = Column(Text, nullable=True)

    def __repr__(self):
        return f"<CollectorLog(status='{self.status}', rows_saved={self.rows_saved})>"