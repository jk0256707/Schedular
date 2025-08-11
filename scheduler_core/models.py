
from django.db import models
from django.utils import timezone


from django.contrib.auth import get_user_model

# class TaskConfig(models.Model):
#     user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="task_configs")
#     name = models.CharField(max_length=100, unique=True)
#     task_type = models.CharField(max_length=100)
#     schedule = models.CharField(max_length=100, help_text="Cron or interval expression")
#     enabled = models.BooleanField(default=True)
#     parameters = models.JSONField(default=dict, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"{self.name} ({'enabled' if self.enabled else 'disabled'})"


# class ScheduledTask(models.Model):
#     STATUS_CHOICES = [
#         ("pending", "Pending"),
#         ("running", "Running"),
#         ("success", "Success"),
#         ("failed", "Failed"),
#     ]
#     config = models.ForeignKey(TaskConfig, on_delete=models.CASCADE, related_name="scheduled_tasks")
#     user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="scheduled_tasks")
#     scheduled_time = models.DateTimeField()
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
#     retries = models.PositiveIntegerField(default=0)
#     last_run = models.DateTimeField(null=True, blank=True)
#     result = models.JSONField(default=dict, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.config.name} at {self.scheduled_time} [{self.status}]"


# class ExecutionLog(models.Model):
#     scheduled_task = models.ForeignKey(ScheduledTask, on_delete=models.CASCADE, related_name="logs")
#     status = models.CharField(max_length=20)
#     started_at = models.DateTimeField(default=timezone.now)
#     finished_at = models.DateTimeField(null=True, blank=True)
#     error = models.TextField(blank=True)
#     output = models.TextField(blank=True)

#     def __str__(self):
#         return f"Log for {self.scheduled_task} ({self.status})"

class Task(models.Model):
    STATUS_CHOICES = [
        ('queued', 'Queued'),
        ('running', 'Running'),
        ('failed', 'Failed'),
        ('success', 'Success'),
    ]
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    command = models.CharField(max_length=255)
    scheduled_time = models.DateTimeField(db_index=True)  # Indexed for efficient range queries
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='queued')
    retry_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    failed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.command} ({self.status})"