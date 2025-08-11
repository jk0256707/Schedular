import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scheduler.settings')

app = Celery('scheduler')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'coordinator-scan-and-dispatch-every-30-seconds': {
        'task': 'coordinator.tasks.coordinator_scan_and_dispatch',
        'schedule': 30.0,
    },
}