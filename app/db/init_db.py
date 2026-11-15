
from app.db.database import Base, engine, SessionLocal
from app.models.entities import Patient, Doctor


def initialize_database():
    # Create all database tables
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        # Insert synthetic patients if none exist
        if db.query(Patient).count() == 0:
            patients = [
                Patient(
                    name="Aarav Sharma",
                    email="aarav@example.test"
                ),
                Patient(
                    name="Meera Singh",
                    email="meera@example.test"
                ),
                Patient(
                    name="Rohan Verma",
                    email="rohan@example.test"
                )
            ]

            db.add_all(patients)

        # Insert doctors if none exist
        if db.query(Doctor).count() == 0:
            doctors = [
                Doctor(
                    name="Dr. Ananya Gupta",
                    specialization="Cardiology"
                ),
                Doctor(
                    name="Dr. Rahul Mehta",
                    specialization="Neurology"
                ),
                Doctor(
                    name="Dr. Priya Kapoor",
                    specialization="Dermatology"
                )
            ]

            db.add_all(doctors)

        db.commit()

        print("Database initialized successfully!")
        print(f"Patients: {db.query(Patient).count()}")
        print(f"Doctors: {db.query(Doctor).count()}")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    initialize_database()
