# BACKEND
cd backend
sudo apt update && sudo apt upgrade -y
python3 --version
pip3 --version
sudo apt install python3-pip
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# FRONTEND
node -v
npm -v
sudo apt update
sudo apt install nodejs npm -y
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt install -y nodejs
sudo apt remove -y nodejs libnode-dev
sudo apt autoremove -y
sudo apt clean
sudo apt update
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt install -y nodejs
node -v
npm -v

npm install
npm start

yarn cache clean
rm -rf ~/.yarn
rm -rf node_modules yarn.lock
yarn install
yarn start

# POSTGRESQL
sudo apt update && sudo apt upgrade -y
sudo apt install postgresql postgresql-contrib -y
sudo systemctl status postgresql
sudo systemctl start postgresql
sudo systemctl enable postgresql


sudo -i -u postgres
psql
CREATE DATABASE mydb;
CREATE USER myuser WITH ENCRYPTED PASSWORD 'mypassword';
GRANT ALL PRIVILEGES ON DATABASE mydb TO myuser;

psql -h localhost -U myuser -d mydb

# OPTIONAL to connect from another machine
sudo nano /etc/postgresql/*/main/postgresql.conf
    #listen_addresses = 'localhost'
    listen_addresses = '*'
sudo nano /etc/postgresql/*/main/pg_hba.conf
    host    all    all    0.0.0.0/0    md5
sudo systemctl restart postgresql

# GUI with PGADMIN
sudo apt install pgadmin4 -y
    Right-click Servers → Register → Server…
        Right-click Servers → Create → ServerGroup…
    Name: LocalPostgres (or any name you like)
    Host name/address: localhost
    Port: 5432 (default Postgres port)
    Maintenance database: mydb
    Username: myuser
    Password: mypassword

# Analytics
Fast prototyping / Python workflow → Streamlit, Dash, Panel, Voila
Scientific / ML dashboards → Panel, Voila, Bokeh, Gradio
Business dashboards (SQL + BI) → Superset, Metabase, Redash
Monitoring / DevOps → Grafana, Kibana
Enterprise-grade BI → Tableau, Power BI, Qlik, Looker

# Datanalytics with Dash
python3 --version
pip3 --version
sudo apt update
sudo apt install python3 python3-pip -y
mkdir datanalytics
cd datanalytics
python3 -m venv dashboard_env
source dashboard_env/bin/activate

# Apache Superset
pip install apache-superset
superset db upgrade
superset fab create-admin
superset load_examples
superset run -p 8088


# DOCKER SETUP
sudo apt remove docker docker-engine docker.io containerd runc
sudo apt update
sudo apt upgrade -y
sudo apt install -y ca-certificates curl gnupg lsb-release
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

docker run -it ubuntu bash
docker ps
docker ps -a
docker images

docker stop <container_id>
docker rm <container_id>

`docker compose up`                       | Build, create, and start all services defined in `docker-compose.yml`. 
`docker compose up -d`                    | Same as above but runs containers **in the background** (detached mode).
`docker compose down`                     | Stop and remove all running containers from the compose file. 
`docker compose stop`                     | Stop running containers without removing them.
`docker compose start`                    | Start previously stopped containers.
`docker compose restart`                  | Restart running containers.  
`docker compose ps`                       | List all containers for the current Compose project.
`docker compose logs`                     | View logs from containers. Add `-f` to **follow logs live*.
`docker compose build`                    | Build or rebuild services without starting them.
`docker compose pull`                     | Pull latest images from Docker Hub.
`docker compose run <service> <command>`  | Run a one-time command inside a service container. Example: `docker compose run web bash`.
`docker compose exec <service> <command>` | Execute a command inside a running container. Example: `docker compose exec db psql -U myuser mydb`.
`docker compose config`                   | Validate your `docker-compose.yml` file and view merged config. 
`docker compose down --volumes`           | Stop containers and remove associated volumes. Useful for full cleanup. 


docker compose up -d                    # Start PostgreSQL + pgAdmin
docker compose up --build -d
docker compose ps                       # See running containers
docker compose logs -f                  # Follow logs
docker compose down                     # Stop and remove containers
docker compose exec <service-name> bash #
docker compose exec db bash

# GIT setup
git clone https://github.com/sojipariola/digital-dentistry-saas.git
cd digital-dentistry-saas

sudo apt update
sudo apt install git -y

git --version
cd ~/Documents/Projects/Dentaloist
git init
git add .
git commit -m "Initial commit"
git remote add origin git@github.com:sojipariola/digital-dentistry-saas.git
git push -u origin main

# CHECKING PORTS
sudo lsof -i :8050
sudo netstat -tulnp | grep 8050
sudo ss -ltnp | grep 8050

sudo kill -9 <PID>
