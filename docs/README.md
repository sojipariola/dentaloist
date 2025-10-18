# 🦷 Digital Dentistry SaaS – Starter Project

This project is a **Flask + React SaaS starter** with:
- Multi-tenant architecture
- JWT authentication
- RBAC (admin, clinic, lab roles)
- Stripe subscription billing (test mode)
- Flask-Admin dashboard (`/admin`)
- React frontend scaffold for consuming APIs
- Swagger/OpenAPI docs (`/docs`)

---

## 🚀 Features
- Flask backend (REST API)
- PostgreSQL database
- Role-based access control (RBAC)
- Stripe subscription billing integration
- Swagger UI API docs
- File uploads with AI placeholder service
- Dockerized services (`api`, `db`, `frontend`)

---

# ⚙️ Local Development Setup (without Docker)

### 📋 Prerequisites
- [Python 3.10+](https://www.python.org/downloads/)
- [Node.js 18+](https://nodejs.org/en/download)
- [PostgreSQL 14+](https://www.postgresql.org/download/)
- [pip](https://pip.pypa.io/en/stable/), [venv](https://docs.python.org/3/library/venv.html)

---

### 1. Clone the repository
```bash
git clone https://github.com/your-org/digital-dentistry-saas.git
cd digital-dentistry-saas



cp -r frontend/src frontend_backup/
cp frontend/package.json frontend_backup/
cp frontend/next.config.ts frontend_backup/
cp frontend/tsconfig.json frontend_backup/
cp frontend/tailwind.config.js frontend_backup/
cp frontend/postcss.config.mjs frontend_backup/
cp frontend/eslint.config.mjs frontend_backup/
cp frontend/next-env.d.ts frontend_backup/




frontend/package.json 
frontend/next.config.ts 
frontend/tsconfig.json 
frontend/tailwind.config.js 
frontend/postcss.config.mjs 
frontend/eslint.config.mjs 
frontend/next-env.d.ts 