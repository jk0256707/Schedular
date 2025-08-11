from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    scheduled_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        input_formats=['%Y-%m-%dT%H:%M'],
        help_text="Select date and time for the task."
    )

    class Meta:
        model = Task
        fields = ['command', 'scheduled_time']
