from datetime import UTC, datetime

from pydantic import BaseModel, Field, field_validator


class AppointmentCreate(BaseModel):
    patient_id: int = Field(gt=0)
    doctor_id: int = Field(gt=0)
    appointment_time: datetime

    @field_validator("appointment_time")
    @classmethod
    def validate_appointment_time(cls, value):
        if value.tzinfo is None:
            raise ValueError("Appointment time must include a timezone")

        if value <= datetime.now(UTC):
            raise ValueError("Appointment must be in the future")

        return value


class AppointmentReschedule(BaseModel):
    appointment_time: datetime

    @field_validator("appointment_time")
    @classmethod
    def validate_appointment_time(cls, value):
        if value.tzinfo is None:
            raise ValueError("Appointment time must include a timezone")

        if value <= datetime.now(UTC):
            raise ValueError("Appointment must be in the future")

        return value


class AppointmentResponse(BaseModel):
    id: int
    patient_id: int
    doctor_id: int
    appointment_time: datetime
    status: str

    class Config:
        from_attributes = True
