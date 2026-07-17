from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import desc
from .database import get_db
from .models import Measurement, CollectorLog
from .collector import save_weather
from datetime import datetime
import pandas as pd
import numpy as np


app = FastAPI(title="Weather API", version="1.0")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def dashboard(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health")
def health():
    return {"status": "ok", "service": "weather-api"}

@app.get("/measurements/latest")
def get_latest(db: Session = Depends(get_db)):
    measurement = db.query(Measurement).order_by(desc(Measurement.recorded_at)).first()
    if not measurement:
        raise HTTPException(status_code=404, detail="No measurements found")
    return {
        "metric": measurement.metric,
        "value": measurement.value,
        "recorded_at": measurement.recorded_at
    }

@app.get("/measurements")
def get_history(
    metric: str = "temperature",
    from_date: str = None,
    to_date: str = None,
    limit: int = 50, 
    db: Session = Depends(get_db)
):
    query = db.query(Measurement).filter(Measurement.metric == metric)
    if from_date:
        query = query.filter(Measurement.recorded_at >= from_date)
    if to_date:
        query = query.filter(Measurement.recorded_at <= to_date)
    results = query.order_by(Measurement.recorded_at).limit(limit).all()
    return [
        {
            "value": m.value,
            "recorded_at": m.recorded_at.isoformat()
        }
        for m in results
    ]

@app.get("/forecast")
def get_forecast(
    metric: str = "temperature",
    n_points: int = 5,
    db: Session = Depends(get_db)
):
    records = db.query(Measurement)\
        .filter(Measurement.metric == metric)\
        .order_by(desc(Measurement.recorded_at))\
        .limit(n_points)\
        .all()
    if len(records) < 2:
        return {"forecast": None, "message": "Not enough data"}
    values = [r.value for r in records]
    forecast = sum(values) / len(values)
    return {
        "metric": metric,
        "forecast": round(forecast, 2),
        "based_on": n_points,
        "last_values": values
    }

@app.get("/anomalies")
def get_anomalies(
    metric: str = "temperature",
    threshold: float = 3.0,
    db: Session = Depends(get_db)
):
    records = db.query(Measurement)\
        .filter(Measurement.metric == metric)\
        .order_by(desc(Measurement.recorded_at))\
        .limit(50)\
        .all()
    if len(records) < 10:
        return {"anomalies": [], "message": "Not enough data"}
    df = pd.DataFrame([{
        "value": r.value,
        "recorded_at": r.recorded_at
    } for r in records])
    mean = df["value"].mean()
    std = df["value"].std()
    anomalies = []
    for _, row in df.iterrows():
        if abs(row["value"] - mean) > threshold * std:
            anomalies.append({
                "value": row["value"],
                "recorded_at": row["recorded_at"].isoformat(),
                "z_score": round((row["value"] - mean) / std, 2)
            })
    return {
        "metric": metric,
        "threshold": threshold,
        "mean": round(mean, 2),
        "std": round(std, 2),
        "anomalies": anomalies[-10:]
    }


@app.on_event("startup")
def startup_event():
    from apscheduler.schedulers.background import BackgroundScheduler
    from apscheduler.triggers.interval import IntervalTrigger
    from .database import SessionLocal
    
    def collect_job():
        db = SessionLocal()
        try:
            save_weather(db)
            print(" Collecte exécutée à {datetime.now()}")
        except Exception as e:
            print(" Erreur collecte: {e}")
        finally:
            db.close()
    
    collect_job()
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        collect_job,
        trigger=IntervalTrigger(minutes=10),
        id="weather_collector",
        replace_existing=True
    )
    scheduler.start()
    print(" Collecteur planifié toutes les 10 minutes")