
# Hospital Management System – Doctor Appointment API

A containerized Doctor Appointment Scheduling API developed as part of the Cloud Deployment & CI/CD internship assignment.

The service allows patients to register, authenticate, create appointments, view appointments, reschedule appointments and cancel appointments.

## 1. Technology Stack

- Python 3.12
- FastAPI
- SQLAlchemy
- PostgreSQL
- SQLite for automated testing
- JWT authentication
- Argon2 password hashing
- Docker and Docker Compose
- Nginx reverse proxy
- GitHub Actions
- Pytest

## 2. Project Structure

```text
Hospital_mgmt_system/
├── app/
│   ├── api/
│   ├── core/
│   ├── db/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   └── main.py
├── tests/
├── docker/
├── nginx/
├── scripts/
├── docs/
├── .github/
│   └── workflows/
│       └── ci-cd.yml
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

## 3. Features

### Authentication
- Patient registration
- User login
- JWT-based authentication
- Password hashing using Argon2
- Protected appointment endpoints

### Appointment Management
- Create appointments
- List appointments
- Reschedule appointments
- Cancel appointments
- Validate patient and doctor references
- Prevent duplicate confirmed appointments for the same doctor and time
- Maintain appointment audit events

### Deployment
- Dockerized API
- PostgreSQL database container
- Persistent database volume
- Nginx reverse proxy
- Health and readiness endpoints
- HTTPS configuration for the local deployment

## 4. Prerequisites

Install the following:

- Python 3.12 or later
- Git
- Docker Desktop
- Docker Compose

## 5. Environment Configuration

Create a `.env` file in the project root.

Use `.env.example` as a reference.

Configure the following variables:

```env
APP_NAME=Hospital Appointment API
APP_ENV=development
DEBUG=False

POSTGRES_PASSWORD=replace_with_a_strong_password
DATABASE_URL=postgresql+psycopg://hospital_user:replace_with_a_strong_password@db:5432/hospital

JWT_SECRET_KEY=replace_with_a_long_random_secret
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Never commit `.env` or production secrets to GitHub.

## 6. Run Locally

Create and activate a virtual environment.

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Start the API:

```bash
uvicorn app.main:app --reload
```

Open the API documentation:

http://127.0.0.1:8000/docs

## 7. Run Using Docker Compose

Make sure Docker Desktop is running.

Build and start the services:

```bash
docker compose up --build -d
```

Check running containers:

```bash
docker compose ps
```

View logs:

```bash
docker compose logs -f
```

Stop the services:

```bash
docker compose down
```

The PostgreSQL database uses a persistent Docker volume.

## 8. API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | /api/auth/register | Register a patient |
| POST | /api/auth/login | Authenticate a patient |
| GET | /api/doctors | List doctors |
| POST | /api/appointments/ | Create appointment |
| GET | /api/appointments/ | List appointments |
| PATCH | /api/appointments/{id}/reschedule | Reschedule appointment |
| PATCH | /api/appointments/{id}/cancel | Cancel appointment |
| GET | /health | Health check |
| GET | /ready | Database readiness check |

Appointment endpoints require a valid JWT bearer token.

## 9. Automated Testing

Run the test suite:

```bash
pytest -v
```

The automated tests cover:

- Unauthenticated access rejection
- Patient appointment creation
- Patient ownership restrictions
- Patient registration
- Duplicate registration prevention
- Patient login

Latest local test result: 6 tests passed.

## 10. CI/CD Pipeline

GitHub Actions automatically runs when code is pushed to the main branch or a pull request targets main.

The workflow performs:

1. Repository checkout
2. Python environment setup
3. Dependency installation
4. Python syntax validation
5. Automated test execution
6. Docker image build

Workflow file:

`.github/workflows/ci-cd.yml`

## 11. Deployment and Security

The deployment uses Docker Compose to run the API and PostgreSQL database.

Nginx acts as a reverse proxy in front of the API.

The project includes:

- Environment-based configuration
- JWT authentication
- Password hashing
- Database persistence
- Container restart policies
- Database health checks
- HTTPS configuration for the local demonstration

The locally generated TLS certificate is self-signed and is intended for demonstration purposes, not public production use.

## 12. Health Checks

API health endpoint:

```text
/health
```

Database readiness endpoint:

```text
/ready
```

These endpoints help verify application availability and database connectivity.

## 13. Repository

GitHub:

https://github.com/Devangana16/Hospital_Management_DevOps

---

**Project:** Hospital Management Platform – Doctor Appointment API  
**Category:** Cloud Deployment & CI/CD  
**Purpose:** Internship technical assignment
