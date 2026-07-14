from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.sql import func
from .database import Base

class Measurement(Base):
    _tablename_ = "measurements"
    
    id = Column(Integer, primary_key=True, index=True)
    source = Column(String, default="open-meteo")
    metric = Column(String, index=True)
    value = Column(Float)
    recorded_at = Column(DateTime, server_default=func.now())

class CollectorLog(Base):
    _tablename_ = "collector_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    run_at = Column(DateTime, server_default=func.now())
    status = Column(String)
    rows_saved = Column(Integer, default=0)
    message = Column(Text, nullable=True)