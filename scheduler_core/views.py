from time import time
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import TaskForm
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from .models import  Task
from .serializers import (
    UserSerializer, TaskConfigSerializer
)

@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = TaskForm(instance=task)
    return render(request, 'scheduler_core/task_update.html', {'form': form, 'task': task})

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('dashboard')
    return render(request, 'scheduler_core/task_confirm_delete.html', {'task': task})


# HTML Frontend Views
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'scheduler_core/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'scheduler_core/login.html', {'form': form})

def logout_view(request):
    auth_logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    if request.user.is_superuser:
        tasks = Task.objects.all()
    else:
        tasks = Task.objects.filter(user=request.user)

    return render(request, 'scheduler_core/dashboard.html', {'tasks': tasks})

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('dashboard')
    else:
        form = TaskForm()
    return render(request, 'scheduler_core/task_form.html', {'form': form})

@login_required
def task_detail(request, pk):
    from django.utils import timezone
    task = get_object_or_404(Task, pk=pk, user=request.user)
    now = timezone.now()
    scheduled_time = task.scheduled_time
    diff = scheduled_time - now
    print(f"Now: {now}")
    print(f"Scheduled Time: {scheduled_time}")
    print(f"Difference: {diff}")
    return render(request, 'scheduler_core/task_detail.html', {'task': task, 'now': now})



class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("email")
        if not username or not password or not email:
            return Response({"error": "Username, password, and email are required."}, status=400)
        if get_user_model().objects.filter(username=username).exists():
            return Response({"error": "Username already exists."}, status=400)
        if get_user_model().objects.filter(email=email).exists():
            return Response({"error": "Email already exists."}, status=400)
        user = get_user_model().objects.create_user(username=username, password=password, email=email)
        return Response(UserSerializer(user).data, status=201)

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key, "user": UserSerializer(user).data})
        return Response({"error": "Invalid credentials."}, status=400)

class TaskConfigViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskConfigSerializer
    permission_classes = [permissions.IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

# class ScheduledTaskViewSet(viewsets.ModelViewSet):
#     queryset = ScheduledTask.objects.all()
#     serializer_class = ScheduledTaskSerializer
#     permission_classes = [permissions.IsAuthenticated]
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)
#     def get_queryset(self):
#         return ScheduledTask.objects.filter(user=self.request.user)

# class ExecutionLogViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = ExecutionLog.objects.all()
#     serializer_class = ExecutionLogSerializer
#     permission_classes = [permissions.IsAuthenticated]
#     def get_queryset(self):
#         return ExecutionLog.objects.filter(scheduled_task__user=self.request.user)
