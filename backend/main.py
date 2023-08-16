from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, Float, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from celery import Celery
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

app = FastAPI()

# Database configuration
DATABASE_URL = "postgresql://postgres:sudarshna@localhost/solar_power_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class SolarPowerData(Base):
    __tablename__ = "solar_power_data"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, index=True)
    solar_power = Column(Float)

# Create the table if it doesn't exist
Base.metadata.create_all(bind=engine)

# Celery configuration
celery = Celery('tasks', broker='redis://localhost:6379/0')

@celery.task
def generate_solar_power_data(start_date, end_date):
    date_range = pd.date_range(start=start_date, end=end_date, freq='H')

    amplitude = 100
    daily_period = 24
    seasonal_period = 24 * 30

    solar_power = amplitude * (np.sin(2 * np.pi * date_range.hour / daily_period) +
                               0.5 * np.sin(2 * np.pi * date_range.hour / seasonal_period))

    data = []
    for timestamp, power in zip(date_range, solar_power):
        data.append({"timestamp": timestamp, "solar_power": power})

    db = SessionLocal()
    for entry in data:
        db_entry = SolarPowerData(**entry)
        db.add(db_entry)
    db.commit()
    db.close()

class TimeSeriesRequest(BaseModel):
    start_date: str
    end_date: str

@app.post("/generate_timeseries/")
async def generate_timeseries(request: TimeSeriesRequest, background_tasks: BackgroundTasks):
    try:
        start_date = pd.to_datetime(request.start_date)
        end_date = pd.to_datetime(request.end_date)
    except ValueError as e:
        print("Error converting dates:", e)
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")

    if start_date >= end_date:
        raise HTTPException(status_code=400, detail="Start date must be before end date.")

    background_tasks.add_task(generate_solar_power_data, start_date, end_date)
    return {"message": "Time series generation started."}

@app.get("/fetch_timeseries/")
async def fetch_timeseries(start_date: str, end_date: str):
    try:
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")

    db = SessionLocal()
    query = db.query(SolarPowerData).filter(
        SolarPowerData.timestamp >= start_date,
        SolarPowerData.timestamp <= end_date
    ).order_by(SolarPowerData.timestamp)
    timeseries_data = query.all()
    db.close()

    return timeseries_data
