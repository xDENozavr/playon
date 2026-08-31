from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """Automatically create a Profile whenever a new User is created -
    covers registration through the site, createsuperuser, shell, etc.,
    not just the register_view flow.
    """
    if created:
        Profile.objects.create(user=instance)