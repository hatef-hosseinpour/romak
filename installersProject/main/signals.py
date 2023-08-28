from .models import Enginroom, locationPublicInfo, EnginRoomPublicInfo, InstallationInfo
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=Enginroom)
def createLocationPublicInfo(sender, instance, created, **kwargs):
    if created:
        locationPublicInfo.objects.create(
            enginroom=instance, user=instance.creator)

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
