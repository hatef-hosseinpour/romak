# File: serializers.py


# @file this serializer convert objects into datatype understandable by frontend, information of Users and Enginroom converted into format understandable for frontend

from rest_framework import serializers
from users.models import Profile
from main.models import Enginroom, locationPublicInfo, EnginRoomPublicInfo, InstallationInfo, EnginRoomImage
from django.contrib.auth.models import User
from .utils import Base64ImageField
from django.core.files.base import ContentFile
import base64
import uuid
import imghdr


# @brief A class for serialize Users objects
class UserSerializers(serializers.ModelSerializer):
    # profile = ProfileSerializer()

    # @brief customize the behavior and characteristics of the User serializer
    class Meta:
        # @param model A User which model whose information is serialized
        model = User
        # @param fields What fields of the User model do we want to serialize
        fields = '__all__'


# @brief This class serialize List of users and their profile
class UserListSerializer(serializers.ModelSerializer):
    # @param using nested serializer for representing User and Profile information together
    user = UserSerializers()

    # @brief customize the behavior and characteristics of the Profile serializer
    class Meta:
        # @param model A Profile which model whose information is serialized
        model = Profile
        # @param fields What fields of the Profile model do we want to serialize
        fields = '__all__'


# @brief A class for serialize Profile objects and decode image that sent from frontend
class ProfileSerializers(serializers.ModelSerializer):
    # @param profile_image the decode image that received from frontend
    profile_image = Base64ImageField(required=True)

    # @brief customize the behavior and characteristics of the Profile serializer
    class Meta:
        # @param model A Profile which model whose information is serialized
        model = Profile
        # @param fields What fields of the Profile model do we want to serialize
        fields = '__all__'


# @brief A class for serialize Enginroom objects
class EnginroomSerializers(serializers.ModelSerializer):

    # @param creator_username this readonly field just for representing username of User that create
    creator_username = serializers.CharField(
        source='creator.username', read_only=True)

    # installer_usernames = serializers.StringRelatedField(
    # source='installer', many=True, read_only=True)

    # @brief customize the behavior and characteristics of the Enginroom serializer
    class Meta:
        # @param model A Enginroom model which model whose information is serialized
        model = Enginroom
        # @param fields What fields of the Enginroom model do we want to serialize
        fields = ['id', 'enginroom_name', 'administration', 'organization',
                  'creator', 'creator_username', 'step']


# @brief A class for serialize Location Public Info objects
class LocationPublicInfoSerializers(serializers.ModelSerializer):
    building_image = Base64ImageField(required=True)
    # @param enginroom_name  this readonly field just to display the name of the engine room where the public information of its location is to be recorded
    enginroom_name = serializers.CharField(
        source='enginroom.enginroom_name', read_only=True)

    # @param installer_username  this readonly field just to display the name of the installer where record public information of engin room
    installer_username = serializers.CharField(
        source='user.username', read_only=True)

    # @brief customize the behavior and characteristics of the LocationPublicInfo serializer
    class Meta:
        # @param model A LocationPublicInfo model which model whose information is serialized
        model = locationPublicInfo
        # @param fields What fields of the LocationPublicInfo model do we want to serialize
        fields = ['id', 'user', 'installer_username', 'enginroom', 'enginroom_name', 'address', 'phone_number1', 'phone_number2',
                  'building_metrage', 'meter_subscription_number', 'building_image', 'location', 'status']


# @brief A class for serialize Location Public Info objects
class EnginroomPublicInfoSerializers(serializers.ModelSerializer):
    # @param installer_username  this readonly field just to display the name of the installer where record public information of engin room
    installer_username = serializers.CharField(
        source='user.username', read_only=True)

    # @param installer_name  this readonly field just to display the name of the installer where record public information of engin room
    installer_name = serializers.SerializerMethodField(read_only=True)

    # @param enginroom_name  this readonly field just to display the name of the engine room where the public information of its location is to be recorded
    enginroom_name = serializers.CharField(
        source='enginroom.enginroom_name', read_only=True)
    # @brief customize the behavior and characteristics of the EnginroomPublicInfo serializer

    class Meta:
        # @param model A EnginroomPublicInfo model which model whose information is serialized
        model = EnginRoomPublicInfo
        # @param fields What fields of the EnginroomPublicInfo model do we want to serialize
        fields = ['id', 'usage', 'has_exchanger', 'number_of_pool_exchangers', 'number_of_jaccuzi_exchangers', 'number_of_floor_heating_exchangers', 'number_of_boilers',
                  'number_of_circulating_pumps', 'number_of_coil_sources', 'number_of_coil_sources_pumps', 'number_of_hot_water_pumps', 'user', 'installer_username', 'enginroom', 'enginroom_name', 'installer_name', 'status']
    # @brief get first name and last name of installer and change them tom format that display in frontend
    # @return full name of installer

    def get_installer_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"


# @brief A class for serialize Installation Info objects
class InstallationInfoSerializers(serializers.ModelSerializer):
    device_serial_number_image = Base64ImageField(required=True)
    # @param installer_username  this readonly field just to display the name of the installer where record public information of engin room
    installer_username = serializers.CharField(
        source='user.username', read_only=True)

    # @param enginroom_name  this readonly field just to display the name of the engine room where the public information of its location is to be recorded
    enginroom_name = serializers.CharField(
        source='enginroom.enginroom_name', read_only=True)

    # @brief customize the behavior and characteristics of the InstallationInfo serializer
    class Meta:
        # @param model A InstallationInfo model which model whose information is serialized
        model = InstallationInfo
        # @param fields What fields of the EnginroomPublicInfo model do we want to serialize
        fields = ['id', 'user', 'installer_username', 'enginroom', 'enginroom_name', 'installed_device_model', 'connection_type',
                  'modem_model', 'has_simcard', 'modem_simcard_number', 'installation_date', 'device_serial_number_image', 'status']

# @brief A class for serialize Enginroom Images objects


class EnginroomImagesSerializers(serializers.ModelSerializer):
    # images_data = serializers.ListField(write_only=True)
    images_data = serializers.ListField(
        child=serializers.CharField(), write_only=True)
    # @param installer_username  this readonly field just to display the name of the installer where record public information of engin room
    installer_username = serializers.CharField(
        source='user.username', read_only=True)

    # @param enginroom_name  this readonly field just to display the name of the engine room where the public information of its location is to be recorded
    enginroom_name = serializers.CharField(
        source='enginroom.enginroom_name', read_only=True)

    # @brief customize the behavior and characteristics of the InstallationInfo serializer
    class Meta:
        # @param model A EnginRoomImage model which model whose information is serialized
        model = EnginRoomImage
        # @param fields What fields of the EnginRoomImage model do we want to serialize
        fields = ['id', 'user', 'installer_username',
                  'enginroom', 'enginroom_name', 'images_data', 'images', 'status']

    def create(self, validated_data):
        images_data = validated_data.pop('images_data')
        split_data = list()
        print('\n\n  len images_data  : \n\n', len(images_data[0].split('data:image/jpeg;base64,')))
        for i in range(1, len(images_data[0].split('data:image/jpeg;base64,'))):
            split_data.append(images_data[0].split('data:image/jpeg;base64,')[i])

        enginroom_images = []

        print('length : ', len(images_data))
        print('length split data : ', len(split_data))
        print('type : ', type(images_data))

        for image_data in split_data:
            enginroom_image = EnginRoomImage.objects.create(**validated_data)
            self.save_image(enginroom_image, image_data)
            enginroom_images.append(enginroom_image)

        return enginroom_images

    def save_image(self, enginroom_image, image_data):
        data = image_data.split(",")[0]
        decoded_data = base64.b64decode(data)
        image_format = imghdr.what(None, decoded_data)

        if not image_format:
            raise serializers.ValidationError("Invalid image format")

        filename = f"{str(uuid.uuid4())}.{image_format}"
        image_file = ContentFile(decoded_data, name=filename)

        enginroom_image.images.save(filename, image_file, save=True)

       
        

