# Copilot Instructions for Dentaloist Codebase

## Overview
This monorepo powers a multi-tenant dental SaaS platform with:
- **Flask backend** (`backend/`): REST API, RBAC, Stripe billing, Flask-Admin, PostgreSQL, multi-tenancy
- **Next.js frontend** (`frontend/`, `next_frontend/`): Modern React UI, role-based dashboards, API integration
- **HTML/JS frontend** (`html_frontend/`): Lightweight, modular UI for rapid prototyping
- **Node.js backend** (`backend_nodejs/`): Auxiliary services (see `server.js`)
- **Database** (`database/`): PostgreSQL setup and docs

## Key Patterns & Conventions
- **Backend models**: All SQLAlchemy models are in `backend/app/models/models.py`. Use explicit relationships and `to_dict()` for serialization. Enum fields use custom types (see `AppointmentType`, `AppointmentStatus`).
- **API**: REST endpoints are in `backend/app/routes/`. Use JWT for auth, RBAC via roles, and Stripe endpoints for billing.
- **Frontend API layer**: All API calls go through `src/lib/api/` (Next.js) or `js/api/` (HTML frontend). TypeScript interfaces in `src/types/` mirror backend models.
- **State management**: Use Zustand (`store/`) in Next.js frontend.
- **Multi-tenancy**: Organization context is required for most backend operations (see `organization_id` fields).
- **Testing**: No single test runner; use `pytest` for backend, `npm test` for frontend. See respective `README.md` for details.
- **Docker**: Use `docker-compose.yml` for full stack dev. Services: `api`, `db`, `frontend`.

## Developer Workflows
- **Backend (Flask):**
  - Install: `pip install -r requirements.txt` in `backend/`
  - Run: `flask run` (set env vars as in `.env.example`)
  - DB Migrations: `flask db migrate`, `flask db upgrade`
  - Admin UI: `/admin` (dev only)
- **Frontend (Next.js):**
  - Install: `npm install` in `frontend/` or `next_frontend/`
  - Run: `npm run dev`
  - API URL: Set `NEXT_PUBLIC_API_URL` in `.env.local`
- **HTML Frontend:**
  - Open `index.html` directly or use `python -m http.server`

## Integration Points
- **Stripe**: Backend endpoints for billing, see `/billing/*` routes
- **RBAC**: Enforced via JWT `role` claim, both backend and frontend
- **Swagger/OpenAPI**: Docs at `/docs` (backend)
- **File Uploads**: Handled by backend, see `uploads/` in `instance/`

## Project Structure Examples
- `backend/app/models/models.py`: All SQLAlchemy models (see `Appointment`, `AvailabilitySlot`)
- `frontend/src/lib/api/`: API service layer
- `frontend/src/types/`: TypeScript interfaces
- `backend/app/routes/`: Flask API endpoints
- `database/SETUP.md`: DB setup instructions

## Special Notes
- **Do not hardcode organization or user IDs**; always use context from JWT or request.
- **When adding models or endpoints, update both backend and frontend types/services.**
- **For new features, follow the patterns in existing models/routes/components.**

---
For more, see `docs/README.md`, `backend/README.md`, and `frontend/README.md`.
