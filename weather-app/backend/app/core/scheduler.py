from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from ..database import SessionLocal
from ..collector import save_weather

scheduler = BackgroundScheduler()


def collect_job():

    db = SessionLocal()

    try:
        save_weather(db)
        print("Weather collected successfully")

    except Exception as e:
        print(f"Collector Error: {e}")

    finally:
        db.close()


def start_scheduler():

    collect_job()

    scheduler.add_job(
        collect_job,
        trigger=IntervalTrigger(minutes=10),
        id="weather_collector",
        replace_existing=True
    )

    scheduler.start()