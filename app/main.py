from app.api.appointments import router as appointment_router
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.init_db import initialize_database
from app.models.entities import Doctor
from app.api.auth import router as auth_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_database()
    yield


app = FastAPI(
    title="Hospital Appointment API",
    description="Doctor Appointment Scheduling Service",
    version="1.0.0",
    lifespan=lifespan
)
app.include_router(appointment_router)
app.include_router(auth_router)

@app.get("/")
def root():
    return {
        "message": "Hospital Appointment API is running",
        "status": "success"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.get("/ready")
def readiness_check(db: Session = Depends(get_db)):
    db.execute(__import__("sqlalchemy").text("SELECT 1"))

    return {
        "status": "ready",
        "database": "connected"
    }


@app.get("/api/doctors")
def list_doctors(db: Session = Depends(get_db)):
    doctors = db.query(Doctor).all()

    return [
        {
            "id": doctor.id,
            "name": doctor.name,
            "specialization": doctor.specialization
        }
        for doctor in doctors
    ]
