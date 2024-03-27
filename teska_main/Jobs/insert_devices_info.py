
import django
import os
import sys
sys.path.append('/home/installersProject')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "installersProject.settings")

django.setup()
from teska_main.models import Device
from main.models import locationPublicInfo, InstallationInfo, EnginRoomPublicInfo
try:
    devices = Device.objects.using('teska_server').all()

    for device in devices:
        serial_number = device.serial_number
        
        if not locationPublicInfo.objects.filter(serial_number=serial_number).exists():
            locationPublicInfo.objects.create(
                device=device.id,
                serial_number=serial_number,
                user=1
            )
            print(f'object of type locationPublicInfo created for device {device.id}')

        if not InstallationInfo.objects.filter(serial_number=serial_number).exists():    
            InstallationInfo.objects.create(
                device=device.id,
                serial_number=serial_number,
                user=1
            )
            print(f'object of type InstallationInfo created for device {device.id}')

        if not EnginRoomPublicInfo.objects.filter(serial_number=serial_number).exists():
            EnginRoomPublicInfo.objects.create(
                device=device.id,
                serial_number=serial_number,
                user=1
            )
            print(f'object of type EnginRoomPublicInfo created for device {device.id}')

except Exception as e:
    print(str(e))
