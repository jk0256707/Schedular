"""scheduler URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from scheduler_core.views import (
    UserViewSet, RegisterView, LoginView, TaskConfigViewSet
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'task-configs', TaskConfigViewSet)
# router.register(r'scheduled-tasks', ScheduledTaskViewSet)
# router.register(r'execution-logs', ExecutionLogViewSet)

from scheduler_core import views as core_views

urlpatterns = [
    path('admin/', admin.site.urls),
    # HTML Frontend
    path('register/', core_views.register, name='register'),
    path('login/', core_views.login_view, name='login'),
    path('logout/', core_views.logout_view, name='logout'),
    path('dashboard/', core_views.dashboard, name='dashboard'),
    path('task/create/', core_views.task_create, name='task_create'),
    path('task/<int:pk>/', core_views.task_detail, name='task_detail'),
    path('task/<int:pk>/update/', core_views.task_update, name='task_update'),
    path('task/<int:pk>/delete/', core_views.task_delete, name='task_delete'),
    # API
    path('api/register/', RegisterView.as_view(), name='api-register'),
    path('api/login/', LoginView.as_view(), name='api-login'),
    path('api/', include(router.urls)),
]
