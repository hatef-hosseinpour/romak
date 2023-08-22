from django.contrib import admin
from .models import Enginroom, locationPublicInfo, EnginRoomPublicInfo,InstallationInfo, EnginRoomImage
# Register your models here.


class EnginRoomPublicInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'enginroom', 'usage', 'has_exchanger', 'number_of_pool_exchangers', 'number_of_jaccuzi_exchangers', 'number_of_floor_heating_exchangers',
                    'number_of_boilers', 'number_of_circulating_pumps', 'number_of_coil_sources', 'number_of_coil_sources_pumps', 'number_of_hot_water_pumps','status']
    list_filter = ['usage', 'has_exchanger', 'status']
    search_fields = ['user__username', 'enginroom__name']
    # fieldsets = (
    #     ('having exchanger', {
    #         'fields':('number_of_pool_exchangers', 'number_of_jaccuzi_exchangers', 'number_of_floor_heating_exchangers')
    #     })
    # ),


class LocationPublicInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'enginroom',
                    'phone_number1', 'phone_number2', 'building_metrage']
    list_filter = ['user', 'enginroom']
    search_fields = ['user__username', 'enginroom__name']


admin.site.register(Enginroom)
admin.site.register(locationPublicInfo, LocationPublicInfoAdmin)
admin.site.register(EnginRoomPublicInfo, EnginRoomPublicInfoAdmin)
admin.site.register(InstallationInfo)
admin.site.register(EnginRoomImage)
