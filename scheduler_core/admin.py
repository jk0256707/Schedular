from django.contrib import admin
from .models import  Task

# @admin.register(TaskConfig)
# class TaskConfigAdmin(admin.ModelAdmin):
#     list_display = ("name", "task_type", "schedule", "enabled", "created_at", "updated_at")
#     search_fields = ("name", "task_type")
#     list_filter = ("enabled",)

# @admin.register(ScheduledTask)
# class ScheduledTaskAdmin(admin.ModelAdmin):
#     list_display = ("config", "scheduled_time", "status", "retries", "last_run", "created_at")
#     search_fields = ("config__name",)
#     list_filter = ("status",)

# @admin.register(ExecutionLog)
# class ExecutionLogAdmin(admin.ModelAdmin):
#     list_display = ("scheduled_task", "status", "started_at", "finished_at")
#     search_fields = ("scheduled_task__config__name", "status")
#     list_filter = ("status",)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("user", "command", "scheduled_time", "status", "retry_count", "created_at")
    search_fields = ("user__username", "command")
    list_filter = ("status", "user")