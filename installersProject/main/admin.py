from django.contrib import admin
from .models import Enginroom, locationPublicInfo, EnginRoomPublicInfo, InstallationInfo, EnginRoomImage
from django.utils.html import format_html


class EnginroomAdmin(admin.ModelAdmin):
    list_display = ['id', 'creator', 'enginroom_name',
                    'organization', 'administration', 'step', 'status']
    list_filter = ['creator', 'organization', 'administration', 'step','status']
    search_fields = ['creator__username', 'enginroom_name']


class EnginRoomPublicInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'enginroom', 'usage', 'has_exchanger', 'number_of_pool_exchangers', 'number_of_jaccuzi_exchangers', 'number_of_floor_heating_exchangers',
                    'number_of_boilers', 'number_of_circulating_pumps', 'number_of_coil_sources', 'number_of_coil_sources_pumps', 'number_of_hot_water_pumps']
    list_filter = ['usage', 'has_exchanger']
    search_fields = ['user__username', 'enginroom__name']


class LocationPublicInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'enginroom',
                    'phone_number1', 'phone_number2', 'building_metrage', 'building_picture', 'location']
    list_filter = ['user', 'enginroom']
    search_fields = ['user__username', 'enginroom__name']

    def building_picture(self, obj):
        return format_html(f'<img src="/images/{obj.building_image} "width="85" height="85""/>')


class InstallationInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'enginroom', 'installed_device_model', 'connection_type', 'modem_model',
                    'has_simcard', 'modem_simcard_number', 'installation_date', 'device_serial_number_picture']
    list_filter = ['user', 'enginroom', 'connection_type', 'installation_date']
    search_fields = ['user__username', 'enginroom__name']

    def device_serial_number_picture(self, obj):
        return format_html(f'<img src="/images/{obj.device_serial_number_image} "width="85" height="85""/>')


class EnginRoomImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'enginroom', 'enginroom_picture']
    list_filter = ['user', 'enginroom']
    search_fields = ['user__username', 'enginroom__name']

    def enginroom_picture(self, obj):
        return format_html(f'<img src="/images/{obj.image} "width="85" height="85""/>')


admin.site.register(Enginroom, EnginroomAdmin)
admin.site.register(locationPublicInfo, LocationPublicInfoAdmin)
admin.site.register(EnginRoomPublicInfo, EnginRoomPublicInfoAdmin)
admin.site.register(InstallationInfo, InstallationInfoAdmin)
admin.site.register(EnginRoomImage, EnginRoomImageAdmin)
