# Full-Stack Development with Flask, React, and PostgreSQL

This tutorial will walk you through building a modern full-stack web application using **Flask** (Python backend), **React** (JavaScript frontend with Node.js tooling), and **PostgreSQL** (database). We’ll cover environment setup, project structure, API design, frontend integration, authentication, and deployment.

---

## 1. Prerequisites

* Python 3.9+ installed
* Node.js 18+ and npm/yarn installed
* PostgreSQL 14+ installed and running
* Git and a code editor (VS Code recommended)

---

## 2. Project Structure

```
project-root/
├── backend/             # Flask API
│   ├── app/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── routes/
│   │   │   └── auth.py
│   │   │   └── appointments.py
│   │   └── utils/
│   ├── migrations/
│   ├── venv/
│   └── run.py
├── frontend/            # React app (Node.js)
│   ├── src/
│   │   ├── App.tsx
│   │   ├── components/
│   │   ├── pages/
│   │   └── api/
│   ├── public/
│   └── package.json
├── database/
│   └── schema.sql
├── docker-compose.yml
├── .env
└── README.md
```

---

## 3. Backend Setup (Flask)

### Create Virtual Environment

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
```

### Install Dependencies

```bash
pip install flask flask_sqlalchemy flask_migrate psycopg2-binary flask-cors python-dotenv
```

### `run.py`

```python
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
```

### `app/__init__.py`

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import os

# Extensions
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    
    # Load configuration
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL", "postgresql://soji:password@localhost:5432/dentaloist"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.appointments import appointments_bp
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(appointments_bp, url_prefix="/api/appointments")

    return app
```

### Example Model (`app/models.py`)

```python
from . import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<User {self.email}>"
```

### Example Route (`app/routes/auth.py`)

```python
from flask import Blueprint, request, jsonify
from app.models import User, db

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    # TODO: hash check
    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({"message": "Login successful", "user": {"id": user.id, "email": user.email}})
    return jsonify({"error": "Invalid credentials"}), 401
```

---

## 4. Database Setup (PostgreSQL)

### Create Database and User

```bash
sudo -i -u postgres
psql
CREATE USER soji WITH PASSWORD 'yourpassword';
CREATE DATABASE dentaloist OWNER soji;
\q
```

### Apply Migrations

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

---

## 5. Frontend Setup (React + Node.js)

### Create React App

```bash
cd frontend
npx create-react-app . --template typescript
```

### Install Dependencies

```bash
npm install axios react-router-dom framer-motion lucide-react
```

### Example API Client (`src/api/client.ts`)

```ts
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
});
```

### Example Login Page (`src/pages/Login.tsx`)

```tsx
import { useState } from 'react';
import { api } from '../api/client';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const res = await api.post('/auth/login', { email, password });
    console.log(res.data);
  };

  return (
    <form onSubmit={handleSubmit}>
      <input value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" />
      <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password" />
      <button type="submit">Login</button>
    </form>
  );
}
```

---

## 6. Connecting Frontend and Backend

* Start Flask backend:

  ```bash
  cd backend
  flask run
  ```
* Start React frontend:

  ```bash
  cd frontend
  npm start
  ```
* The React app will call Flask API endpoints at `http://localhost:5000/api/...`

---

## 7. Authentication

* Use **JWT tokens** for secure authentication.
* Flask: `pip install flask-jwt-extended`
* Add JWT setup in backend.
* Store token in `localStorage` on frontend.

---

## 8. Deployment

### Option 1: Docker + Docker Compose

`docker-compose.yml`

```yaml
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=postgresql://soji:yourpassword@db:5432/dentaloist
    depends_on:
      - db

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"

  db:
    image: postgres:14
    environment:
      POSTGRES_USER: soji
      POSTGRES_PASSWORD: yourpassword
      POSTGRES_DB: dentaloist
    ports:
      - "5432:5432"
```

### Option 2: Cloud Deployment

* Backend: Deploy Flask app to **Heroku / Render / AWS ECS**
* Frontend: Deploy React app to **Vercel / Netlify**
* Database: Use **AWS RDS / Railway / Supabase**

---

## 9. Next Steps

* Add Role-based Access Control
* Implement file uploads (S3 bucket)
* Integrate third-party APIs (Google, GitHub login)
* Add automated tests with `pytest` and `jest`

---

## 10. Resources

* [Flask Documentation](https://flask.palletsprojects.com/)
* [React Docs](https://react.dev/)
* [SQLAlchemy Docs](https://docs.sqlalchemy.org/)
* [PostgreSQL Docs](https://www.postgresql.org/docs/)
* [Docker Compose Docs](https://docs.docker.com/compose/)

---

✅ You now have a full-stack setup: **Flask backend**, **Postgres database**, and **React frontend** with Node.js tooling.
