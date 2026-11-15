from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.database import get_db
from app.models.entities import Appointment, AuditEvent, Doctor, Patient, User
from app.schemas.appointment import (
    AppointmentCreate,
    AppointmentReschedule,
    AppointmentResponse,
)

router = APIRouter(prefix="/api/appointments", tags=["Appointments"])


def record_audit(db, action, appointment):
    event = AuditEvent(
        action=action,
        entity_type="appointment",
        entity_id=appointment.id,
        details=f"Appointment {appointment.id}: {action}",
        created_at=datetime.now(UTC),
    )
    db.add(event)


@router.post(
    "/", response_model=AppointmentResponse, status_code=status.HTTP_201_CREATED
)
def create_appointment(
    data: AppointmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    patient = (
        db.query(Patient)
        .filter(Patient.id == data.patient_id, Patient.email == current_user.email)
        .first()
    )

    doctor = db.query(Doctor).filter(Doctor.id == data.doctor_id).first()

    if not patient:
        raise HTTPException(404, "Patient not found")

    if not doctor:
        raise HTTPException(404, "Doctor not found")

    appointment = Appointment(
        patient_id=data.patient_id,
        doctor_id=data.doctor_id,
        appointment_time=data.appointment_time,
        status="confirmed",
    )

    try:
        db.add(appointment)
        db.flush()

        record_audit(db, "appointment_created", appointment)
        db.commit()
        db.refresh(appointment)

        return appointment

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="This doctor already has a confirmed appointment at that time",
        )


@router.get("/", response_model=list[AppointmentResponse])
def list_appointments(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    if current_user.role == "admin":
        return db.query(Appointment).all()

    patient = db.query(Patient).filter(Patient.email == current_user.email).first()

    if not patient:
        return []

    return db.query(Appointment).filter(Appointment.patient_id == patient.id).all()


@router.patch("/{appointment_id}/reschedule", response_model=AppointmentResponse)
def reschedule_appointment(
    appointment_id: int,
    data: AppointmentReschedule,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Appointment).filter(Appointment.id == appointment_id)

    if current_user.role != "admin":
        patient = db.query(Patient).filter(Patient.email == current_user.email).first()

        if not patient:
            raise HTTPException(403, "Patient record not found")

        query = query.filter(Appointment.patient_id == patient.id)

    appointment = query.first()

    if not appointment:
        raise HTTPException(404, "Appointment not found")

    if appointment.status != "confirmed":
        raise HTTPException(400, "Only confirmed appointments can be rescheduled")

    appointment.appointment_time = data.appointment_time

    try:
        record_audit(db, "appointment_rescheduled", appointment)
        db.commit()
        db.refresh(appointment)
        return appointment

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409, detail="The requested time slot is already booked"
        )


@router.patch("/{appointment_id}/cancel")
def cancel_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Appointment).filter(Appointment.id == appointment_id)

    if current_user.role != "admin":
        patient = db.query(Patient).filter(Patient.email == current_user.email).first()

        if not patient:
            raise HTTPException(403, "Patient record not found")

        query = query.filter(Appointment.patient_id == patient.id)

    appointment = query.first()

    if not appointment:
        raise HTTPException(404, "Appointment not found")

    if appointment.status != "confirmed":
        raise HTTPException(400, "Appointment is not confirmed")

    appointment.status = "cancelled"

    record_audit(db, "appointment_cancelled", appointment)
    db.commit()

    return {
        "message": "Appointment cancelled successfully",
        "appointment_id": appointment.id,
    }
