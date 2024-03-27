import base64
import imghdr
import uuid
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from rest_framework import serializers
from jdatetime import datetime as jalali_dt
from datetime import datetime

class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        data = data.split(",")[-1]
        decoded_data = base64.b64decode(data)
        image_format = imghdr.what(None, decoded_data)

        if not image_format:
            raise serializers.ValidationError("Invalid image format")

        # Create a temporary image object to check for rotation
        temp_image = Image.open(BytesIO(decoded_data))
        
        # Initialize rotation number
        rotation_number = None

        # Correct orientation if necessary and print rotation number
        if hasattr(temp_image, '_getexif'):
            orientation = 0x0112
            exif = temp_image._getexif()
            if exif is not None and orientation in exif:
                rotation_number = exif[orientation]
                rotations = {
                    1: "No rotation",
                    3: "180°",
                    6: "90° CCW",
                    8: "90° CW"
                }
                print(f"Rotation number: {rotation_number} ({rotations.get(rotation_number, 'Unknown')})")

        # Convert the PIL image back to bytes
        with BytesIO() as output:
            temp_image.save(output, format=image_format)
            image_data = output.getvalue()

        filename = f"{str(uuid.uuid4())}.{image_format}"
        image_file = ContentFile(image_data, name=filename)
        return super().to_internal_value(image_file)

def convertToJalali(gregorian_dt):
    dt = datetime.strptime(gregorian_dt, '%Y-%m-%dT%H:%M:%S.%f%z')
    j_dt = jalali_dt.fromgregorian(datetime=dt)
    j_dt = j_dt.strftime('%Y-%m-%d %H:%M:%S')

    return j_dt
    



