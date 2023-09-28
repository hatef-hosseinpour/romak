from .models import Enginroom, locationPublicInfo, EnginRoomPublicInfo, InstallationInfo, EnginRoomImage
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
import os


@receiver(post_save, sender=Enginroom)
def createLocationPublicInfo(sender, instance, created, **kwargs):
    if created:
        locationPublicInfo.objects.create(
            enginroom=instance, user=instance.creator)
    else:
        instance. locationpublicinfo.save()

@receiver(pre_delete, sender=locationPublicInfo)
def deleteBuildingImage(sender, instance, **kwargs):
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

@receiver(pre_delete, sender=InstallationInfo)
def deleteProfileImage(sender, instance, **kwargs):
    if os.path.isfile(instance.device_serial_number_image.path) and 'no-image.jpg' not in instance.device_serial_number_image.path:
        os.remove(instance.device_serial_number_image.path)


@receiver(pre_delete, sender=EnginRoomImage)
def deleteProfileImage(sender, instance, **kwargs):
    if os.path.isfile(instance.images.path) and 'no-image.jpg' not in instance.images.path:
        os.remove(instance.images.path)
