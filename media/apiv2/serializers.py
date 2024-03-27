from rest_framework import serializers
from teska_main.models import Device, Organization, Location, EngineRoomFeature
from django.contrib.auth.models import User


class DeviceSerializer(serializers.ModelSerializer):
    organization_id = serializers.PrimaryKeyRelatedField(
        source='organization.id', read_only=True)
    # location_id = serializers.PrimaryKeyRelatedField(
    # source='location.id', read_only=True)
    organization = serializers.CharField(
        source='organization.organization', read_only=True)
    main_3d_view = serializers.CharField(
        source='engine_room_feature.main_3d_view', read_only=True)

    administration = serializers.CharField(
        source='organization.administration', read_only=True)
    province = serializers.CharField(
        source='location.province', read_only=True)
    # created_by
    city = serializers.CharField(
        source='location.city', read_only=True)

    creator = serializers.SerializerMethodField(read_only=True)

    installer_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Device
        fields = '__all__'

    def get_creator(self, obj):
        created_by_id = obj.created_by

        try:
            user = User.objects.get(id=created_by_id)
            username = user.username
            return username
        except User.DoesNotExist:
            return None
        
    def get_installer_name(self, obj):
        created_by_id = obj.created_by

        try:
            user = User.objects.get(id=created_by_id)
            name = user.first_name + ' ' + user.last_name
            return name
        except User.DoesNotExist:
            return None


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class EngineRoomFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngineRoomFeature
        fields = '__all__'
