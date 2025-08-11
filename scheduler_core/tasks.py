
from celery import shared_task
from .models import Task
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
import subprocess

# def simulate_task_run(task_command):
#     start = timezone.now()
#     print(f"[SIM] Task '{task_name}' started at {start}", file=sys.stdout)
#     subprocess.run()
#     end = timezone.now()
#     print(f"[SIM] Task '{task_name}' ended at {end} (duration: {wait}s)", file=sys.stdout)
#     return {"started": str(start), "ended": str(end), "duration": wait}

@shared_task(bind=True, max_retries=3)
def execute_scheduled_task(self, scheduled_task_id):
    print("-----------------------SCHEDULED TASK--------------------------------\n", scheduled_task_id)
    try:
        task = Task.objects.get(id=scheduled_task_id)
        task.status = "running"
        task.started_at = timezone.now()
        task.save()
        # Simulate task execution with random wait and print
        print(type(task.command))
        print(task.command)
        result = subprocess.run(task.command, shell=True, capture_output=True, text=True, timeout=300)
        if result.returncode == 0:
            task.status = 'success'
            task.finished_at = timezone.now()
            task.save()
        else:
            raise Exception(result.stderr)        
    except Exception as exc:
        task.retry_count += 1
        task.status = 'failed'
        task.failed_at = timezone.now()
        task.save()
        if task.retry_count >= 5:
            send_mail(
                'Task Failed Multiple Times',
                f'Task {task.id} failed 5 times. Last error: {exc}',
                settings.DEFAULT_FROM_EMAIL,
                [task.user.email],
            )
        else:
            raise self.retry(exc=exc, countdown=60 * (2 ** task.retry_count))
    else:
        task.save()