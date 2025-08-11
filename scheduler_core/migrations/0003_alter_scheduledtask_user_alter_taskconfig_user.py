# Generated manually to handle user field constraints properly
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def set_default_user_for_existing_records(apps, schema_editor):
    """
    Set a default user for existing records that have NULL user fields.
    This is a data migration to handle existing data properly.
    """
    TaskConfig = apps.get_model('scheduler_core', 'TaskConfig')
    ScheduledTask = apps.get_model('scheduler_core', 'ScheduledTask')
    User = apps.get_model(settings.AUTH_USER_MODEL)
    
    # Get the first superuser as default, or create one if none exists
    try:
        default_user = User.objects.filter(is_superuser=True).first()
        if not default_user:
            # Create a default admin user if none exists
            default_user = User.objects.create_user(
                username='admin',
                email='admin@example.com',
                is_superuser=True,
                is_staff=True
            )
    except Exception:
        # If we can't create a user, we'll handle this in the database constraint
        return
    
    # Update TaskConfig records with NULL user
    TaskConfig.objects.filter(user__isnull=True).update(user=default_user)
    
    # Update ScheduledTask records with NULL user
    ScheduledTask.objects.filter(user__isnull=True).update(user=default_user)


def reverse_set_default_user(apps, schema_editor):
    """
    Reverse migration - set user fields back to NULL
    """
    # We don't reverse this as it would break data integrity
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler_core', '0002_scheduledtask_user_taskconfig_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        # First, run the data migration to populate NULL values
        migrations.RunPython(
            set_default_user_for_existing_records,
            reverse_set_default_user,
        ),
        
        # Then alter the fields to be non-nullable
        migrations.AlterField(
            model_name='scheduledtask',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scheduled_tasks', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='taskconfig',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task_configs', to=settings.AUTH_USER_MODEL),
        ),
    ]
