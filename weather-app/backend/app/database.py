from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from .config import Config


if Config.DATABASE_URL.startswith("sqlite"):

    engine = create_engine(
        Config.DATABASE_URL,
        connect_args={
            "check_same_thread": False
        }
    )

else:

    engine = create_engine(
        Config.DATABASE_URL
    )



SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


Base = declarative_base()



def init_db():

    from . import models

    Base.metadata.create_all(
        bind=engine
    )

    print("Database initialized")



def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()