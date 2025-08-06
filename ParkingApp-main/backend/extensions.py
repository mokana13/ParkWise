# backend/extensions.py
from flask_mail import Mail
from celery import Celery

mail = Mail()
celery = Celery(__name__, broker='redis://localhost:6379/0')
