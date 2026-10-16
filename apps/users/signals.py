from django.db.models.signals import post_delete
from django.dispatch import receiver

from apps.users.models import EmployeeProfile


@receiver(post_delete, sender=EmployeeProfile)
def delete_orphaned_user(sender, instance, **kwargs):
    # If the profile is deleted, delete the associated User to prevent dangling auth records
    try:
        if instance.user:
            instance.user.delete()
    except Exception:  # noqa
        # User is already deleted or being deleted by cascade
        pass
