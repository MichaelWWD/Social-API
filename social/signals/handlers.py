from django.dispatch import receiver
from django.conf import settings
from django.db.models.signals import post_save
from ..models import Profile

User = settings.AUTH_USER_MODEL

@receiver(post_save, sender=User)
def create_social_profile_for_new_user(sender, **kwargs):
    if kwargs['created']:
        Profile.objects.create(user=kwargs['instance'])
