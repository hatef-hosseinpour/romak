from django.db import models
from django.contrib.auth.models import User


class Organization(models.Model):
    organization = models.CharField(max_length=100, default='')
    administration  = models.CharField(max_length=100, default='')
    # owners = models.ManyToManyField(User, blank=True)

    class Meta:
        managed = False
        db_table = 'main_organization'

class Location(models.Model):
    city = models.CharField(max_length=100, default='')
    province = models.CharField(max_length=100, default='')
    
    class Meta:
        managed = False
        db_table = 'main_location'

class EngineRoomFeature(models.Model):
    main_3d_view = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return str(self.main_3d_view)
    class Meta:
        managed = False
        db_table = 'main_engineroomfeature'

class Device(models.Model):
    # created_at = models.DateTimeField(verbose_name='created at', auto_now_add=True)
    # updated_at = models.DateTimeField(verbose_name='updated at', auto_now=True)
    name = models.CharField(verbose_name='device name', max_length=100)
    serial_number = models.CharField(max_length=100, unique=True)
    # api_key = models.OneToOneField(APIKey, on_delete=models.PROTECT, editable=False, null=True)
    key = models.CharField(blank=True, max_length=100, editable=True, unique=True)
    installation_address = models.CharField(max_length=500, default='')
    # owners = models.ManyToManyField(User, blank=True)
    active = models.BooleanField(default=True)
    engine_room_feature = models.ForeignKey(EngineRoomFeature, on_delete=models.PROTECT, editable=True, null=True)
    location = models.ForeignKey(Location, on_delete=models.PROTECT, editable=True, null=True)
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT, editable=True, null=True)


    step = models.IntegerField(default=0, blank=True, null=True)
    status = models.BooleanField(default=None, blank=True, null=True)
    rejection_note = models.TextField(default='', blank=True, null=True)
    created_by = models.IntegerField(default=1, blank=True, null=True)
    details = models.JSONField(null=True)
    lat_long = models.CharField(max_length=100,  default='', blank=True, null=True)


    class Meta:
        managed = False
        db_table = 'main_device'
        ordering = ['-id']

    # def get_api_key(self):
    #     api_key, key = APIKey.objects.create_key(name=self.name)
    #     return api_key, key
# Create your models here.
