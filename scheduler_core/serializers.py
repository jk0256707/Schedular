from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import  Task

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    class Meta:
        model = User
        fields = ["id", "username", "email"]

class TaskConfigSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Task
        fields = "__all__"

# class ScheduledTaskSerializer(serializers.ModelSerializer):
#     user = UserSerializer(read_only=True)
#     config = TaskConfigSerializer(read_only=True)
#     class Meta:
#         model = ScheduledTask
#         fields = "__all__"

# class ExecutionLogSerializer(serializers.ModelSerializer):
#     scheduled_task = ScheduledTaskSerializer(read_only=True)
#     class Meta:
#         model = ExecutionLog
#         fields = "__all__"
