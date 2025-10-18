# Switch to postgres user
sudo -u postgres psql

-- Create your user with a password
CREATE USER olusoji WITH PASSWORD 'Soji1111';

-- Create the database
CREATE DATABASE dentaloist;

-- Grant privileges to your user
GRANT ALL PRIVILEGES ON DATABASE dentaloist TO olusoji;

-- Make the user a superuser (for development only)
ALTER USER olusoji WITH SUPERUSER;

-- Exit
\q



# Remove database and migrations
rm -rf instance/ app.db migrations/ __pycache__ */__pycache__

# (optional, only if you have .pytest_cache or other cache folders)
rm -rf .pytest_cache

mkdir -p instance
touch instance/app.db
chmod 664 instance/app.db

# Initialize Alembic
flask db init

# Generate migration scripts
flask db migrate -m "Initial migration"

# Apply migrations
flask db upgrade
