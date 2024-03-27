
import django
import os
import sys
import logging
sys.path.append(
    'D:\\Romak System\\Projects\\InstallersProject\\installersProject')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "installersProject.settings")

django.setup()
from teska_main.models import Organization, Device
from main.models import Enginroom, User
try:

    logger = logging.getLogger('root')

    organizations = Organization.objects.using('teska_server').all()
    devices = Device.objects.using('teska_server').all()
    engineroom_ids = Enginroom.objects.values_list('id', flat=True)
    admin = User.objects.get(username='admin')

    for device in devices:
        # Check if the device ID is not already in Enginroom
        if device.id not in engineroom_ids:
            Enginroom.objects.create(
                id = device.id,
                enginroom_name=device.name,
                creator=admin,
                organization=device.organization.organization,
                administration=device.organization.administration,
                step=0,
                status=None,
                rejection_note='',
                serial_number=device.serial_number
            )

    logger.info(f'Inserting Devices successfully')
    print('done')


except Exception as e:
    logger.error(f'Error Inseting devices: {str(e)}')
