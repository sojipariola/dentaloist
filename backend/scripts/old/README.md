# Digital Dentistry Platform – Flask SaaS Starter (Extended)

This extended scaffold adds RBAC, Stripe billing endpoints, Flask-Admin, and a simple React admin dashboard scaffold.

## What's new
- Role-Based Access Control (RBAC) through JWT `role` claim.
- Stripe integration endpoints (`/billing/create-checkout-session`, `/billing/webhook`).
- Flask-Admin UI mounted at `/admin` for quick admin operations (dev only).
- Simple React admin dashboard in `frontend/` that can login and call API.

## Quick Start (Docker)
1. Copy env and launch:
```
cp .env.example .env
docker compose up --build -d
```
2. Initialize DB:
```
docker compose exec api flask db init
docker compose exec api flask db migrate -m "init"
docker compose exec api flask db upgrade
```
3. Visit:
- API: http://localhost:8000
- Swagger: http://localhost:8000/docs
- Admin (Flask-Admin): http://localhost:8000/admin
- Frontend: http://localhost:3000 (run frontend separately)

## Frontend
The `frontend/` folder contains a React app that demonstrates login, viewing patients, and creating checkout sessions.

## Notes
- Replace Stripe test keys in `.env` before using billing features.
- Flask-Admin `is_accessible` is permissive for dev; implement proper admin auth in production.
