

use Fake, create an update of cli.py  to add 3 organizations at 'FREE' subscription level, with each an admin staff, a dentist, an nurse and maximum possible number of patients for  'FREE' subscription level and populate all database tables 

rm -r instance         # or wherever your DB file is
rm -r migrations       # deletes old Alembic migrations
flask db init          # only if you deleted migrations folder
mkdir instance
flask db migrate -m "Initial migration"
flask db upgrade



sudo -i -u postgres
psql
\du
# Basic SQL Query in postgres
sudo -u postgres psql
\l
\c dentaloist
\dt
SELECT id, email, first_name, last_name, role FROM users LIMIT 5;
SELECT id, email, first_name, last_name, organization_id, role FROM users LIMIT 5;
\d users
\d appointments
\d patients
\d organizations
CREATE USER Olusoji WITH PASSWORD 'Soji1111';

ALTER USER Olusoji WITH PASSWORD 'Soji1111';
CREATE DATABASE dentaloist;
GRANT ALL PRIVILEGES ON DATABASE dentaloist TO olusoji;

psql -h 127.0.0.1 -U olusoji -d dentaloist
psql -h localhost -U olusoji -d dentaloist
psql -h <host> -U <username> -d <database>
DROP TABLE IF EXISTS alembic_version;

psql -U postgres

# -- Get basic column information
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_name = 'users'
ORDER BY ordinal_position;

# more detail column information
SELECT 
    column_name,
    data_type,
    character_maximum_length,
    is_nullable,
    column_default,
    ordinal_position
FROM information_schema.columns
WHERE table_name = 'users'
ORDER BY ordinal_position;

# 1️⃣ Ensure PostgreSQL is Running
From your project root (Dentaloist/):
docker compose up -d db
    User: olusoji
    Password: Soji1111
    Database: mydb
    Port: 5432

# Optional: connect via psql to create a test user:
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

INSERT INTO users (email, password)
VALUES ('test@dentaloist.com', '$2b$12$J1u0...') -- bcrypt hash
ON CONFLICT DO NOTHING;

# 2️⃣ Install Dependencies in Next.js
From your frontend folder:
cd frontend
npm install bcrypt pg prisma

bcrypt → hash/verify passwords
pg → PostgreSQL driver

prisma → optional ORM (simplifies DB access)

# 3️⃣ Create DB Connection (lib/db.js)
import { Pool } from "pg";
import bcrypt from "bcrypt";

const pool = new Pool({
  user: "olusoji",
  host: "localhost",   // use 'db' if running inside Docker Compose network
  database: "mydb",
  password: "Soji1111",
  port: 5432,
});

export async function findUserByEmail(email) {
  const res = await pool.query("SELECT * FROM users WHERE email=$1", [email]);
  return res.rows[0];
}

export async function hashCompare(password, hash) {
  return bcrypt.compare(password, hash);
}

# 4️⃣ Create Login API (pages/api/auth/login.js)
import { findUserByEmail, hashCompare } from "../../../lib/db";

export default async function handler(req, res) {
  if (req.method !== "POST")
    return res.status(405).json({ message: "Method not allowed" });

  const { email, password } = req.body;
  const user = await findUserByEmail(email);

  if (user && (await hashCompare(password, user.password))) {
    return res.status(200).json({ message: "Login successful", userId: user.id });
  }

  return res.status(401).json({ message: "Invalid credentials" });
}

# 5️⃣ Create Frontend Login Page (pages/login.js)
import { useState } from "react";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [msg, setMsg] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch("/api/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });
      const data = await res.json();
      setMsg(data.message);
    } catch (err) {
      setMsg("Login failed");
    }
  };

  return (
    <form onSubmit={handleLogin} style={{ padding: "2rem" }}>
      <h2>Dentaloist Login</h2>
      <input type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} /><br /><br />
      <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} /><br /><br />
      <button type="submit">Login</button>
      <p>{msg}</p>
    </form>
  );
}

# 6️⃣ Run the Project
Start backend DB:
docker compose up -d db

Run Next.js frontend:
npm run dev

Visit:
http://localhost:3000/login


Test login with your test user (test@dentaloist.com + password).

✅ Key Notes

If you run frontend in Docker, change host: "localhost" → host: "db" in lib/db.js.

Passwords in DB must be hashed with bcrypt:

bcrypt.hashSync("mypassword", 12)


No CORS issues — Next.js API and frontend are served from same host (3000).

This setup gives you full end-to-end login:
Frontend → Next.js API → PostgreSQL → Response → Frontend.




# Apply the empty migration
flask db upgrade
# Backup if needed
cp instance/app.db instance/app.db.backup
# Reset everything
flask shell
  from app import db
  db.drop_all()
  print("✅ All tables dropped")
  db.create_all()
  print("✅ All tables recreated")
  exit()

# Create and apply clean migration
rm -rf migrations
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

