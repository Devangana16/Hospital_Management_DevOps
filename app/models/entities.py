
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Text,
    Index,
    text,
    Boolean
)
from sqlalchemy.orm import relationship
from app.db.database import Base


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)

    appointments = relationship(
        "Appointment",
        back_populates="patient"
    )


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    specialization = Column(String(100), nullable=False)

    appointments = relationship(
        "Appointment",
        back_populates="doctor"
    )


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)

    patient_id = Column(
        Integer,
        ForeignKey("patients.id"),
        nullable=False
    )

    doctor_id = Column(
        Integer,
        ForeignKey("doctors.id"),
        nullable=False
    )

    appointment_time = Column(DateTime, nullable=False)
    status = Column(String(20), default="confirmed", nullable=False)

    patient = relationship(
        "Patient",
        back_populates="appointments"
    )

    doctor = relationship(
        "Doctor",
        back_populates="appointments"
    )


# Prevent two active appointments for the same doctor and time.
Index(
    "uq_active_doctor_appointment_time",
    Appointment.doctor_id,
    Appointment.appointment_time,
    unique=True,
    sqlite_where=text("status = 'confirmed'"),
    postgresql_where=text("status = 'confirmed'")
)


class AuditEvent(Base):
    __tablename__ = "audit_events"

    id = Column(Integer, primary_key=True, index=True)
    action = Column(String(100), nullable=False)
    entity_type = Column(String(100), nullable=False)
    entity_id = Column(Integer, nullable=True)
    details = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    email = Column(
        String(150),
        unique=True,
        nullable=False,
        index=True
    )

    hashed_password = Column(
        String(255),
        nullable=False
    )

    role = Column(
        String(20),
        nullable=False,
        default="patient"
    )

    is_active = Column(
        Boolean,
        default=True,
        nullable=False
    )
