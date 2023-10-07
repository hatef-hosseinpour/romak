# File: models.py
# @File
# This is the file for define main models of project

from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# @brief The class for Enginroom


class Enginroom(models.Model):
    # @param name creator the id of the user that create this enginroom
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, editable=True, null=True, default=None, related_name='created_enginrooms')
    # @param name enginroom_name the name of this enginroom
    enginroom_name = models.CharField(max_length=200, null=True, blank=True)
    # @param name organization the name of organization of this enginroon
    organization = models.CharField(max_length=200, null=True, blank=True)
    # @param name administration the name of administration of this enginroon
    administration = models.CharField(max_length=200, null=True, blank=True)

    # @param step to findout which step of installation is filled
    step = models.PositiveIntegerField(default=0, null=True, blank=True)

    # @param status this field defaul to false after user fill information of installation admin can accept it and after accept of admin this field change to true
    status = models.BooleanField(default=None, null=True)

    rejection_note = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['-id']

    def __str__(self) -> str:
        return '%s' % self.enginroom_name

# @brief The class for Public Info of Location of Installation device


class locationPublicInfo(models.Model):
    # @param user the use id of fill this informations
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, editable=True, null=True, default=None)
    # @param enginroom this data is about this enginroom
    enginroom = models.OneToOneField(
        Enginroom, on_delete=models.CASCADE, editable=True, null=True, default=None)
    # @param address the address of this enginroom
    address = models.TextField(null=True, blank=True)

    province = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    # @param phone number 1 the phone number of Contact phone number 1
    phone_number1 = models.CharField(max_length=20, null=True, blank=True)
    # @param phone number 1 the phone number of Contact phone number 2
    phone_number2 = models.CharField(max_length=20, null=True, blank=True)
    # @param building metrage the metrage of this building
    building_metrage = models.PositiveIntegerField(
        default=0, null=True, blank=True)
    # @param meter_subscription_number the number of subscription of this meter
    meter_subscription_number = models.CharField(
        max_length=200, null=True, blank=True)
    # @param building_image the image of the building that device installed
    building_image = models.ImageField(
        null=True, blank=True, upload_to='building_images/', default='no-image.jpg', max_length=200)
    # @param location the location of this building that chosen from map and coordination of it stored in this field
    location = models.CharField(max_length=200, null=True, blank=True)
    # @param status this field defaul to false after user fill information of installation admin can accept it and after accept of admin this field change to true
    # status = models.BooleanField(default=False, null=True)

    def __str__(self) -> str:
        return "%s" % self.enginroom

    # @brief save building image in specific size
    # @return the image that has size of 300*300
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.building_image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.building_image.path)

# @brief this class for Public information of enginroom


class EnginRoomPublicInfo(models.Model):
    USAGE_TYPE = (
        ('heating', 'گرمایشی'),
        ('sanitary', 'آبگرم بهداشتی'),
        ('both', 'هردو'),
    )
    # @param user the use id of fill this informations
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, editable=True, null=True, default=None)
    # @param enginroom this data is about this enginroom
    enginroom = models.OneToOneField(
        Enginroom, on_delete=models.CASCADE, editable=True, null=True, default=None)
    usage = models.CharField(
        max_length=2000, choices=USAGE_TYPE, null=True, blank=True)
    has_exchanger = models.BooleanField(default=False)

    # if user set has_exchanger field to True, user can fill three blow fields
    number_of_pool_exchangers = models.PositiveIntegerField(default=0)
    number_of_jaccuzi_exchangers = models.PositiveIntegerField(default=0)
    number_of_floor_heating_exchangers = models.PositiveIntegerField(default=0)

    number_of_boilers = models.PositiveIntegerField(default=0)
    number_of_circulating_pumps = models.PositiveIntegerField(default=0)
    number_of_coil_sources = models.PositiveIntegerField(default=0)
    number_of_coil_sources_pumps = models.PositiveIntegerField(default=0)
    number_of_hot_water_pumps = models.PositiveIntegerField(default=0)

    # @param status this field defaul to false after user fill information of installation admin can accept it and after accept of admin this field change to true
    # status = models.BooleanField(default=False, null=True)

    def __str__(self) -> str:
        return f'{self.enginroom} با کاربری {self.usage}'


class InstallationInfo(models.Model):
    DEVICE_MODEL = (
        ('8relays', '8relays'),
        ('12relays', '12relays'),
        ('16relays', '16relays')
    )
    CONNECTION = (
        ('internet', 'internet'),
        ('intranet', 'intranet'),
        ('ethernet', 'ethernet'),
    )
    # @param user the use id of fill this informations
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, editable=True, null=True, default=None)
    # @param enginroom this data is about this enginroom
    enginroom = models.OneToOneField(
        Enginroom, on_delete=models.CASCADE, editable=True, null=True, default=None)
    # @param installed_device_model the model of device that can be in 3 value 8relays, 12relays, 16relays
    installed_device_model = models.CharField(
        max_length=2000, choices=DEVICE_MODEL, null=True, blank=True)
    # @param connection_type the type of modem connection that can be in 3 value internet, intranet, ethernet
    connection_type = models.CharField(
        max_length=2000, choices=CONNECTION, null=True, blank=True)
    # @param modem_model model of model that use in this enginroom
    modem_model = models.CharField(max_length=200, null=True, blank=True)
    # @param has_simcard check that model has simcard or not
    has_simcard = models.BooleanField(default=False, null=True)

    # @param modem_simcard_number if user set has_simcard field to True, user can fill simcard number fields
    modem_simcard_number = models.CharField(
        max_length=200, null=True, blank=True)
    # @param  installation_date the date and time of installation
    # @param  modem_serial_number_image the user should take a picture from serial of modem number
    modem_simcard_serial_number_image = models.ImageField(
        null=True, blank=True, upload_to='modem_simcard_serial_number_images/', default='no-image.jpg')
    installation_date = models.CharField(max_length=1000,
        verbose_name='installed_at', null=True, blank=True)
    # @param  device_serial_number_image the user should take a picture from serial of device number
    device_serial_number_image = models.ImageField(
        null=True, blank=True, upload_to='device_serial_number_images/', default='no-image.jpg')
    # @param status this field defaul to false after user fill information of installation admin can accept it and after accept of admin this field change to true
    # status = models.BooleanField(default=False, null=True)

    def __str__(self) -> str:
        return f'{self.installed_device_model} installed at {str(self.installation_date)}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.device_serial_number_image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.device_serial_number_image.path)


class EnginRoomImage(models.Model):
    # # @param installtion the id of installation info every image belong to installtion
    # installation = models.ForeignKey(
    #     InstallationInfo, on_delete=models.CASCADE, editable=True, null=True, default=None)
    # @param user the use id of fill this informations
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, editable=True, null=True, default=None)
    # @param enginroom this data is about this enginroom
    enginroom = models.ForeignKey(
        Enginroom, on_delete=models.CASCADE, editable=True, null=True, default=None)
    # @param image in this table each enginroom can have any images
    image = models.ImageField(
        null=True, blank=True, upload_to='enginroom_images/')
    # @param status this field defaul to false after user fill information of installation admin can accept it and after accept of admin this field change to true
    # status = models.BooleanField(default=False, null=True)

    def __str__(self):

        return f'Image {self.id}  - Enginroom {self.enginroom.enginroom_name}'

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)

    #     img = Image.open(self.image.path)
    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)
