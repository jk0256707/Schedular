# coordinator/tasks.py
from celery import shared_task
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail

from scheduler_core.models import Task

@shared_task
def coordinator_scan_and_dispatch():
    now = timezone.now()
    next_31s = now + timezone.timedelta(seconds=31)
    due_tasks = Task.objects.filter(status='queued', scheduled_time__lte=next_31s)
    print("-----------------------DUE TASK--------------------------------\n", due_tasks)
    for task in due_tasks:
        # Dispatch to worker (Celery task) 
        from scheduler_core.tasks import execute_scheduled_task
        execute_scheduled_task.apply_async(args=[task.id], eta=task.scheduled_time)

# Optionally, add retry/worker liveness logic here or in separate tasks
