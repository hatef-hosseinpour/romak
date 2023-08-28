from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete
from .models import Profile
from django.dispatch import receiver
import os


@receiver(post_save, sender=User)
def createProfile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()


@receiver(pre_delete, sender=Profile)
def deleteProfileImage(sender, instance, **kwargs):
    if os.path.isfile(instance.profile_image.path) and 'default_user.jpg' not in instance.profile_image.path:
        os.remove(instance.profile_image.path)
