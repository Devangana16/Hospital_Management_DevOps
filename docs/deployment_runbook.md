
# Hospital Appointment API – Deployment and Recovery Runbook

## 1. Purpose

This runbook describes the deployment, monitoring, troubleshooting, backup and recovery procedures for the Hospital Appointment API.

## 2. Deployment Requirements

The following tools are required:

- Docker Desktop
- Docker Compose
- Git
- Windows PowerShell or Command Prompt

## 3. Environment Configuration

Before deployment:

1. Create the `.env` file in the project root.
2. Configure the PostgreSQL password.
3. Configure a strong JWT secret.
4. Verify the database connection string.
5. Ensure that `.env` is excluded from Git.

## 4. Starting the Application

Navigate to the project directory:

```bash
cd Hospital_mgmt_system
```

Build and start all containers:

```bash
docker compose up --build -d
```

Verify the containers:

```bash
docker compose ps
```

Expected services:

- hospital_api
- hospital_db
- hospital_nginx

The database should report a healthy status.

## 5. Application Health Monitoring

Check the API health endpoint:

```bash
curl.exe -I http://localhost
```

Check the HTTPS endpoint:

```bash
curl.exe -k -I https://localhost
```

Check the API readiness endpoint:

```bash
curl.exe -k https://localhost/ready
```

Expected readiness response:

```json
{
  "status": "ready",
  "database": "connected"
}
```

The `-k` option is used because the local demonstration uses a self-signed TLS certificate.

## 6. Viewing Application Logs

View all container logs:

```bash
docker compose logs
```

View API logs:

```bash
docker compose logs api
```

View database logs:

```bash
docker compose logs db
```

Follow logs continuously:

```bash
docker compose logs -f
```

## 7. Restart and Recovery

Restart all services:

```bash
docker compose restart
```

Restart only the API:

```bash
docker compose restart api
```

If a container stops unexpectedly, inspect its logs:

```bash
docker compose logs api
```

Check container status:

```bash
docker compose ps -a
```

Rebuild and restart the application if required:

```bash
docker compose up --build -d
```

## 8. Database Backup

Create a backup directory:

```bash
mkdir backups
```

Create a PostgreSQL backup:

```bash
docker compose exec -T db pg_dump -U hospital_user hospital > backups/hospital_backup.sql
```

Verify that the backup file exists:

```bash
dir backups
```

The backup should be stored securely and must not be committed to GitHub.

## 9. Database Restore

**Warning:** Restoring a database can replace existing data. Perform this operation only when authorized and after securing a separate backup.

Restore the SQL backup:

```powershell
Get-Content -Raw .\backups\hospital_backup.sql | docker compose exec -T db psql -U hospital_user -d hospital
```

Verify database connectivity:

```bash
docker compose exec db pg_isready -U hospital_user -d hospital
```

Verify the application:

```bash
curl.exe -k https://localhost/ready
```

## 10. Stopping the Application

Stop containers without deleting persistent database data:

```bash
docker compose down
```

Do not use `docker compose down -v` unless you intentionally want to remove the database volume and its stored data.

## 11. Rollback Procedure

If a newly built application version causes problems:

1. Inspect the application logs.
2. Identify the last known working application version.
3. Stop the affected application.
4. Redeploy the previously verified Docker image or source revision.
5. Check the API health and readiness endpoints.
6. Verify appointment operations.

A versioned image or Git commit should be retained before deployment to support rollback.

## 12. Security Precautions

- Never commit `.env` files.
- Use strong database credentials.
- Use a strong JWT secret.
- Restrict database access to the internal Docker network.
- Do not expose PostgreSQL publicly.
- Use valid TLS certificates for production.
- Keep dependencies and container images updated.
- Store database backups securely.

## 13. Recovery Verification Checklist

- [ ] PostgreSQL container is healthy.
- [ ] API container is running.
- [ ] Nginx container is running.
- [ ] API health endpoint responds.
- [ ] Database readiness endpoint responds.
- [ ] Database backup file exists.
- [ ] Database restore has been tested.
- [ ] Appointment API operations work after recovery.
