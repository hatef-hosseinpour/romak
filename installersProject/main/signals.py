from .models import Enginroom, locationPublicInfo, EnginRoomPublicInfo, InstallationInfo
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
import os


@receiver(post_save, sender=Enginroom)
def createLocationPublicInfo(sender, instance, created, **kwargs):
    if created:
        locationPublicInfo.objects.create(
            enginroom=instance, user=instance.creator)

@receiver(pre_delete, sender=locationPublicInfo)
def deleteProfileImage(sender, instance, **kwargs):
    if os.path.isfile(instance.building_image.path) and 'no-image.jpg' not in instance.building_image.path:
        os.remove(instance.building_image.path)

@receiver(post_save, sender=Enginroom)
def createEnginRoomPublicInfo(sender, instance, created, **kwargs):
    if created:
        EnginRoomPublicInfo.objects.create(
            enginroom=instance, user=instance.creator)
    else:
        instance.enginroompublicinfo.save()

@receiver(post_save, sender=Enginroom)
def createInstallationInfo(sender, instance, created, **kwargs):
    if created:
        InstallationInfo.objects.create(
            enginroom=instance, user=instance.creator)
    else:
        instance.installationinfo.save()
