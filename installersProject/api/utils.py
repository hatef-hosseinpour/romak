from django.core.files.base import ContentFile
from rest_framework import serializers
import base64
import uuid
import imghdr


class Base64ImageField(serializers.ImageField):

    def to_internal_value(self, data):
        data = data.split(",")[-1]
        decoded_data = base64.b64decode(data)
        image_format = imghdr.what(None, decoded_data)

        if not image_format:
            raise serializers.ValidationError("Invalid image format")

        filename = f"{str(uuid.uuid4())}.{image_format}"
        image_file = ContentFile(decoded_data, name=filename)
        return super().to_internal_value(image_file)
