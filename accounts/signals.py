from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from .models import Profile

# Create a profile after a user is created
@receiver(post_save, sender=User) 
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)