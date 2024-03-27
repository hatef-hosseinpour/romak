from django.contrib import admin
from .models import locationPublicInfo, EnginRoomPublicInfo, InstallationInfo, EnginRoomImage, EventHistory
from teska_main.models import Device
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.ttfonts import TTFont
from django.conf import settings
from reportlab.pdfbase import pdfmetrics
from django.utils.html import format_html
from .utils import get_model_as_csv_file_response


class DeviceMixin:
    def get_device_name(self, obj):
        try:
            device = Device.objects.using('teska_server').get(id=obj.device)
            return device.name
        except Device.DoesNotExist:
            return "Unknown"
    get_device_name.short_description = "Device Name"

    def get_installer_name(self, obj):
        try:
            device = Device.objects.using('teska_server').get(id=obj.device)
            installer = User.objects.get(id=device.created_by)
            return installer.username
        except Exception:
            return "Unknown"
    get_installer_name.short_description = "installer username"


def generate_pdf(modeladmin, request, queryset):

    buffer = BytesIO()
    font_file_path = str(settings.BASE_DIR / "static/fonts/Vazir.ttf")
    pdfmetrics.registerFont(TTFont('Persian', font_file_path))
    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer, pagesize=A4)

    # Set initial y-coordinate for drawing text
    y_coordinate = 800

    # Draw column headers
    p.drawString(100, y_coordinate, "ID")
    p.drawString(200, y_coordinate, "User")
    p.drawString(300, y_coordinate, "address")
    # Add more column headers as needed

    # Adjust y-coordinate for next row
    y_coordinate -= 20

    # Draw data on the PDF.
    for obj in queryset:
        # address = obj.address.encode('utf-8') if obj.address is not None else b""
        # Draw information on the PDF
        p.drawString(100, y_coordinate, str(obj.id))
        p.drawString(200, y_coordinate, str(obj.user))
        p.drawString(300, y_coordinate, str(obj.address).encode('utf-8'))
        # Add more fields as needed

        # Adjust y-coordinate for next row
        y_coordinate -= 20

    # Close the PDF object cleanly.
    p.showPage()
    p.save()

    # Set the buffer's pointer to the beginning.
    buffer.seek(0)
    # Serve the generated PDF file as a response.
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="hello.pdf"'
    return response


generate_pdf.short_description = "Generate PDF"


def export_model(self, request, queryset):
    model = queryset.model
    fields = [field.name for field in model._meta.get_fields()]
    meta = {
        'file': f'/{model._meta.model_name}.csv',
        'queryset': queryset,
        'fields': fields
    }
    return get_model_as_csv_file_response(meta, content_type='text/csv')


export_model.short_description = 'Export as CSV'


class EnginRoomPublicInfoAdmin(DeviceMixin, admin.ModelAdmin):
    list_display = ['id', 'get_installer_name', 'get_device_name', 'usage', 'has_exchanger', 'number_of_pool_exchangers', 'number_of_jaccuzi_exchangers', 'number_of_floor_heating_exchangers',
                    'number_of_boilers', 'number_of_circulating_pumps', 'number_of_coil_sources', 'number_of_coil_sources_pumps', 'number_of_hot_water_pumps']
    list_filter = ['usage', 'has_exchanger']
    search_fields = ['user__username']
    actions = [export_model]


class LocationPublicInfoAdmin(DeviceMixin, admin.ModelAdmin):
    list_display = ['id', 'get_installer_name', 'get_device_name',
                    'phone_number1', 'phone_number2', 'building_metrage', 'building_picture']
    list_filter = ['user', 'device']
    search_fields = ['user', 'device']
    actions = [export_model, generate_pdf]

    def building_picture(self, obj):
        return format_html(f'<img src="/media/{obj.building_image} "width="85" height="85""/>')


class InstallationInfoAdmin(DeviceMixin, admin.ModelAdmin):
    list_display = ['id', 'get_installer_name', 'get_device_name', 'installed_device_model', 'connection_type', 'modem_model',
                    'has_simcard', 'modem_simcard_number', 'installation_date', 'device_serial_number_picture']
    list_filter = ['user', 'device', 'connection_type', 'installation_date']
    # search_fields = ['user', 'enginroom__name']

    def device_serial_number_picture(self, obj):
        return format_html(f'<img src="/media/{obj.device_serial_number_image} "width="85" height="85""/>')


class EnginRoomImageAdmin(DeviceMixin, admin.ModelAdmin):
    list_display = ['id', 'get_installer_name', 'get_device_name', 'device_picture']
    list_filter = ['user', 'device']
    search_fields = ['user__username', 'device__name']

    def device_picture(self, obj):
        return format_html(f'<img src="/media/{obj.image} "width="85" height="85""/>')


admin.site.register(locationPublicInfo, LocationPublicInfoAdmin)
admin.site.register(EnginRoomPublicInfo, EnginRoomPublicInfoAdmin)
admin.site.register(InstallationInfo, InstallationInfoAdmin)
admin.site.register(EnginRoomImage, EnginRoomImageAdmin)
admin.site.register(EventHistory)
