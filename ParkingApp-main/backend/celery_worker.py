from celery import Celery
from celery.schedules import crontab

celery = Celery(
    'parking_app',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0',
    include=['backend.tasks.background']  # Ensure your tasks are loaded
)

celery.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

celery.conf.beat_schedule = {
    # Daily reminder at 18:00 UTC (which is 11:30 PM IST)
    'send-daily-reminders': {
        'task': 'tasks.send_daily_reminders',
        'schedule': crontab(hour=18, minute=0),
    },
    # Monthly report on the 1st at 00:00 UTC
    'generate-monthly-reports': {
        'task': 'tasks.generate_monthly_reports',
        'schedule': crontab(hour=0, minute=0, day_of_month=1),
    },
}

