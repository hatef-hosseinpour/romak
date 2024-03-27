
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

        
        if not Device.objects.using('teska_server').filter(serial_number=serial_number).exists():
            
            location_public_info = locationPublicInfo.objects.create(
                device=device.id, serial_number=serial_number, user=1)

            
            installation_info = InstallationInfo.objects.create(
                device=device.id, serial_number=serial_number, user=1)

            # Create EnginRoomPublicInfo
            engin_room_public_info = EnginRoomPublicInfo.objects.create(
                device=device.id, serial_number=serial_number, user=1)

    print('done')

except Exception as e:
    print(str(e))