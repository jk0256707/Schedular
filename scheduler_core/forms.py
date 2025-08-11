from django import forms
from .models import Task

class TaskForm(forms.ModelForm):

    def clean_scheduled_time(self):
        from django.utils import timezone
        scheduled_time = self.cleaned_data['scheduled_time']
        if scheduled_time <= timezone.now():
            raise forms.ValidationError("Scheduled time must be in the future.")
        return scheduled_time
    
    scheduled_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        input_formats=['%Y-%m-%dT%H:%M'],
        help_text="Select date and time for the task."
    )

    class Meta:
        model = Task
        fields = ['command', 'scheduled_time']
