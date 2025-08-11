from django import template
from datetime import timedelta
from django.utils import timezone

register = template.Library()

@register.filter
def time_diff(scheduled_time):
    """
    Returns the difference between two datetimes as 'Xm Ys'.
    """
    diff = scheduled_time - timezone.now()
    if diff.total_seconds() < 0:
        return "0m 0s"
    minutes, seconds = divmod(int(diff.total_seconds()), 60)
    return f"{minutes}m {seconds}s"
