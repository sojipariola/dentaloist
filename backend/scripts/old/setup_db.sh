#!/bin/bash
# save as setup_db.sh

# Set variables
DB_NAME="dentaloist_db"
DB_USER="olusoji"
DB_PASSWORD="secure_password_123"

# Create user and database
sudo -u postgres psql -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';"
sudo -u postgres psql -c "CREATE DATABASE $DB_NAME;"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"

# Update .env file
echo "DATABASE_URL=postgresql://$DB_USER:$DB_PASSWORD@localhost:5432/$DB_NAME" >> .env
echo "DB_HOST=localhost" >> .env
echo "DB_PORT=5432" >> .env
echo "DB_NAME=$DB_NAME" >> .env
echo "DB_USER=$DB_USER" >> .env
echo "DB_PASSWORD=$DB_PASSWORD" >> .env

echo "✅ Database setup complete!"
