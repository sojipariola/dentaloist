# app/scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from app.utils.usage_alert import check_and_alert_usage

scheduler = BackgroundScheduler()
scheduler.add_job(check_and_alert_usage, 'interval', minutes=60)
scheduler.start()
