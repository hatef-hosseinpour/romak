from django.shortcuts import get_object_or_404
import requests
from django.conf import settings
from rest_framework.views import APIView
from teska_main.models import Device, Organization, EngineRoomFeature, Location
from django.contrib.auth.models import User
from main.models import locationPublicInfo, InstallationInfo, EnginRoomPublicInfo, EventHistory
from .serializers import DeviceSerializer, OrganizationSerializer, EngineRoomFeatureSerializer, LocationSerializer, DeviceListSerializer
from rest_framework.response import Response
from rest_framework import generics, status, permissions, viewsets
from rest_framework.decorators import action
from api.pagination import CustomEngineroomPagination
import logging
import json
from .utils import DataEncryptionAgent
from rest_framework import status
import re
from django.db.models import Q, F
from .utils import get_object_by_user, get_device_status

logger = logging.getLogger(__name__)


class ListObjectsAPIView(generics.ListAPIView):
    model_serializer_map = {
        'device': (Device, DeviceSerializer),
        'organization': (Organization, OrganizationSerializer),
        'engineroomfeature': (EngineRoomFeature, EngineRoomFeatureSerializer),
        'location': (Location, LocationSerializer),
    }

    serializer_class = None
    permission_classes = [
        permissions.IsAuthenticated | permissions.IsAdminUser]
    pagination_class = CustomEngineroomPagination

    def get_serializer_class(self):
        model_name = self.kwargs.get('model_name', '').lower()

        model_class, serializer_class = self.model_serializer_map.get(
            model_name, (None, None))

        if not model_class or not serializer_class:
            return None

        return serializer_class

    def get_queryset(self):
        model_name = self.kwargs.get('model_name', '').lower()

        model_class, serializer_class = self.model_serializer_map.get(
            model_name, (None, None))

        if not model_class:
            return None

        queryset = model_class.objects.using('teska_server').all()

        search_query = self.request.query_params.get('search', None)
        if model_name == 'device':

            queryset = get_object_by_user(self.request.user, queryset)

            installer = self.request.query_params.get('installer')
            organization = self.request.query_params.get('organization')
            administration = self.request.query_params.get('administration')
            province = self.request.query_params.get('province')
            city = self.request.query_params.get('city')

            if search_query:
                queryset = queryset.filter(Q(name__icontains=search_query) | Q(
                    organization__organization__icontains=search_query) | Q(
                    organization__administration__icontains=search_query))

            if installer:
                queryset = queryset.filter(created_by=installer)

            if organization:
                queryset = queryset.filter(
                    organization__organization=organization)

            if administration:
                queryset = queryset.filter(
                    organization__administration=administration)

            if province:
                queryset = queryset.filter(location__province=province)

            if city:
                queryset = queryset.filter(location__city=city)
        elif model_name == 'organization':
            search_query = self.request.query_params.get('search', None)

            if search_query:
                queryset = queryset.filter(Q(organization__icontains=search_query) | Q(
                    administration__icontains=search_query))

        elif model_name == 'location':
            search_query = self.request.query_params.get('search', None)

            if search_query:
                queryset = queryset.filter(
                    Q(province__icontains=search_query) | Q(city__icontains=search_query))

        elif model_name == 'engineroomfeature':
            search_query = self.request.query_params.get('search', None)

            if search_query:
                queryset = queryset.filter(
                    main_3d_view__icontains=search_query)

        

        return queryset

    def get(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset().order_by('-id')
            # Get count of filtered queryset
            queryset_count = queryset.count()
            
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(queryset, many=True)
            model_class = serializer_class.Meta.model.__name__
            page = self.paginate_queryset(serializer.data)
            logger.info(f'{model_class} list successfully returned.')
            return self.get_paginated_response(page)

        except Exception as e:
            logger.error(str(e))
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class RetrieveObjectsAPIView(generics.RetrieveAPIView, ListObjectsAPIView):
    def retrieve(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer_class = self.get_serializer_class()
            instance = self.get_object()
            serializer = serializer_class(instance)
            model_class = serializer_class.Meta.model.__name__
            logger.info(f'Information of {model_class} loaded')
            return Response(serializer.data)
        except Exception as e:
            logger.error(str(e))
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


########################################### Device List ###############################################
class ListDevicesAPIView(generics.ListAPIView):
    serializer_class = DeviceListSerializer
    permission_classes = [
        permissions.IsAuthenticated | permissions.IsAdminUser]
    pagination_class = CustomEngineroomPagination

class ListDevicesAPIView(generics.ListAPIView):
    serializer_class = DeviceListSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomEngineroomPagination

    def get_queryset(self):
        queryset = Device.objects.using('teska_server').all()
        
        # Filter queryset based on user
        queryset = get_object_by_user(self.request.user, queryset)

        # Retrieve query parameters
        search_query = self.request.query_params.get('search')
        installer = self.request.query_params.get('installer')
        organization = self.request.query_params.get('organization')
        administration = self.request.query_params.get('administration')
        province = self.request.query_params.get('province')
        city = self.request.query_params.get('city')

        # Apply filters
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(organization__organization__icontains=search_query) |
                Q(organization__administration__icontains=search_query)|
                Q(location__province__icontains=search_query)|
                Q(location__city__icontains=search_query)
            )

        if installer:
            queryset = queryset.filter(created_by=installer)

        if organization:
            queryset = queryset.filter(organization__organization=organization)

        if administration:
            queryset = queryset.filter(organization__administration=administration)


        if province:
            queryset = queryset.filter(location__province=province)

        if city:
            queryset = queryset.filter(location__city=city)

        return queryset
########################################### Device List ###############################################




class CreateObjectApiView(generics.CreateAPIView):

    model_serializer_map = {
        'device': (Device, DeviceSerializer),
        'organization': (Organization, OrganizationSerializer),
        'engineroomfeature': (EngineRoomFeature, EngineRoomFeatureSerializer),
        'location': (Location, LocationSerializer),
    }

    serializer_class = None
    permission_classes = [
        permissions.IsAuthenticated | permissions.IsAdminUser]
    # pagination_class = CustomEngineroomPagination

    def get_serializer_class(self):
        try:
            model_name = self.kwargs.get('model_name', '').lower()

            model_class, serializer_class = self.model_serializer_map.get(
                model_name, (None, None))

            if not model_class or not serializer_class:
                return None

            return serializer_class
        except Exception as e:
            logger.error(f'error: {str(e)}')
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        model_name = self.kwargs.get('model_name', '').lower()
        model_class, serializer_class = self.model_serializer_map.get(
            model_name, (None, None))

        if not model_class or not serializer_class:
            return Response({'error': 'Invalid model'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = serializer_class(data=request.data)
        encryption_agent = DataEncryptionAgent()
        if model_name == 'organization':
            organization = request.data.get('organization')
            administration = request.data.get('administration')
            if Organization.objects.using('teska_server').filter(organization=organization).exists():
                logger.warning('Organization already exist')
                return Response({'message': "already exist"}, status=status.HTTP_409_CONFLICT)

            else:
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': f'Api-Key {settings.API_KEY}'
                }

                body = {
                    'object_type': 'Organization',
                    'organization': organization,
                    'administration': administration
                }

                body_json = json.dumps(body)
                encrypted_body = encryption_agent.encrypt(body_json)

                # Prepare encrypted data
                encrypted_data = {'ciphertext': encrypted_body}

                response = requests.post(
                    settings.API_URL, json=encrypted_data, headers=headers)
                txt = response.text
                response_data = json.loads(txt)
                ciphertext = response_data['ciphertext']
                decrypted_response = encryption_agent.decrypt(ciphertext)
                if response.status_code == 200:
                    decrypted_response = encryption_agent.decrypt(ciphertext)
                    logger.info(
                        f'Organization {organization} added successfully.')
                    return Response({'message': f'{decrypted_response}'}, status=status.HTTP_201_CREATED)
                else:
                    logger.error(
                        f'Error in adding organization {organization}.')
                    return Response({'error': decrypted_response}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        elif model_name == 'location':
            city = request.data.get('city')
            province = request.data.get('province')
            if Location.objects.using('teska_server').filter(city=city, province=province).exists():
                logger.warning('Location already exist')
                return Response({'message': "already exist"}, status=status.HTTP_409_CONFLICT)

            else:
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': f'Api-Key {settings.API_KEY}'
                }

                body = {
                    'object_type': 'Location',
                    'city': city,
                    'province': province
                }

                body_json = json.dumps(body)
                encrypted_body = encryption_agent.encrypt(body_json)

                # Prepare encrypted data
                encrypted_data = {'ciphertext': encrypted_body}

                response = requests.post(
                    settings.API_URL, json=encrypted_data, headers=headers)

                if response.status_code == 200:
                    txt = response.text
                    response_data = json.loads(txt)
                    ciphertext = response_data['ciphertext']
                    decrypted_response = encryption_agent.decrypt(ciphertext)
                    logger.info(
                        f'Location  {province},{city} added successfully.')
                    return Response({'message': f'{decrypted_response}'}, status=status.HTTP_201_CREATED)
                else:
                    logger.error(
                        f'Error in adding Location  {province},{city}.')
                    return Response({'error': 'Failed to add Location'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        elif model_name == 'engineroomfeature':
            main_3d_view = request.data.get('main_3d_view')
            if EngineRoomFeature.objects.using('teska_server').filter(main_3d_view=main_3d_view).exists():
                logger.warning('EngineRoomFeature already exist')
                return Response({'message': "already exist"}, status=status.HTTP_409_CONFLICT)

            else:

                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': f'Api-Key {settings.API_KEY}'
                }

                body = {
                    'object_type': 'EngineRoomFeature',
                    'main_3d_view': main_3d_view,

                }
                body_json = json.dumps(body)
                encrypted_body = encryption_agent.encrypt(body_json)

                # Prepare encrypted data
                encrypted_data = {'ciphertext': encrypted_body}

                response = requests.post(
                    settings.API_URL, json=encrypted_data, headers=headers)
                txt = response.text
                response_data = json.loads(txt)
                ciphertext = response_data['ciphertext']
                decrypted_response = encryption_agent.decrypt(ciphertext)
                if response.status_code == 200:
                    logger.info(
                        f'EngineRoomFeature {main_3d_view} added successfully.')
                    return Response({'message': f'{decrypted_response}'}, status=status.HTTP_201_CREATED)
                else:
                    logger.error(
                        f'error in add EngineRoomFeature {main_3d_view}, error msg: {decrypted_response}')
                    return Response({'error': decrypted_response}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return super().create(request, *args, **kwargs)


class UpdateObjectApiView(generics.CreateAPIView):
    model_serializer_map = {
        'device': (Device, DeviceSerializer),
        'organization': (Organization, OrganizationSerializer),
        'engineroomfeature': (EngineRoomFeature, EngineRoomFeatureSerializer),
        'location': (Location, LocationSerializer),
    }

    serializer_class = None
    permission_classes = [
        permissions.IsAuthenticated | permissions.IsAdminUser]
    # pagination_class = CustomEngineroomPagination

    def get_serializer_class(self):
        try:
            model_name = self.kwargs.get('model_name', '').lower()

            model_class, serializer_class = self.model_serializer_map.get(
                model_name, (None, None))

            if not model_class or not serializer_class:
                return None

            return serializer_class
        except Exception as e:
            logger.error('Location already exist')
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        model_name = self.kwargs.get('model_name', '').lower()
        model_class, serializer_class = self.model_serializer_map.get(
            model_name, (None, None))

        if not model_class or not serializer_class:
            return Response({'error': 'Invalid model'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = serializer_class(data=request.data)
        encryption_agent = DataEncryptionAgent()
        if model_name == 'organization':
            organization = request.data.get('organization')
            organization_id = request.data.get('id')
            administration = request.data.get('administration')

            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Api-Key {settings.API_KEY}'
            }

            body = {
                'object_type': 'Organization',
                'id': organization_id,
                'organization': organization,
                'administration': administration
            }

            body_json = json.dumps(body)
            encrypted_body = encryption_agent.encrypt(body_json)

            # Prepare encrypted data
            encrypted_data = {'ciphertext': encrypted_body}

            response = requests.put(
                settings.EDIT_API_URL, json=encrypted_data, headers=headers)
            txt = response.text
            response_data = json.loads(txt)
            ciphertext = response_data['ciphertext']
            decrypted_response = encryption_agent.decrypt(ciphertext)
            if response.status_code == 200:
                decrypted_response = encryption_agent.decrypt(ciphertext)
                logger.info(
                    f'Organization {organization} edited successfully.')
                return Response({'message': f'{decrypted_response}'}, status=status.HTTP_200_OK)
            else:
                logger.error(
                    f'Error in editing organization {organization}.')
                return Response({'error': decrypted_response}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        elif model_name == 'location':
            city = request.data.get('city')
            province = request.data.get('province')
            location_id = request.data.get('id')
            # if Location.objects.using('teska_server').filter(city=city, province=province).exists():
            #     return Response({'message': "already exist"}, status=status.HTTP_409_CONFLICT)

            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Api-Key {settings.API_KEY}'
            }

            body = {
                'object_type': 'Location',
                'id': location_id,
                'city': city,
                'province': province
            }

            body_json = json.dumps(body)
            encrypted_body = encryption_agent.encrypt(body_json)

            # Prepare encrypted data
            encrypted_data = {'ciphertext': encrypted_body}

            response = requests.put(
                settings.EDIT_API_URL, json=encrypted_data, headers=headers)

            if response.status_code == 200:
                txt = response.text
                response_data = json.loads(txt)
                ciphertext = response_data['ciphertext']
                decrypted_response = encryption_agent.decrypt(ciphertext)
                logger.info(
                    f'Location  {province},{city} edited successfully.')
                return Response({'message': f'{decrypted_response}'}, status=status.HTTP_200_OK)
            else:
                logger.error(
                    f'Error in editing Location  {province},{city}.')
                return Response({'error': 'Failed to add Location'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        elif model_name == 'engineroomfeature':
            main_3d_view = request.data.get('main_3d_view')
            feature_id = request.data.get('id')
            # if EngineRoomFeature.objects.using('teska_server').filter(main_3d_view=main_3d_view).exists():
            #     return Response({'message': "already exist"}, status=status.HTTP_409_CONFLICT)

            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Api-Key {settings.API_KEY}'
            }

            body = {
                'object_type': 'EngineRoomFeature',
                'id': feature_id,
                'main_3d_view': main_3d_view,

            }
            body_json = json.dumps(body)
            encrypted_body = encryption_agent.encrypt(body_json)

            # Prepare encrypted data
            encrypted_data = {'ciphertext': encrypted_body}

            response = requests.put(
                settings.EDIT_API_URL, json=encrypted_data, headers=headers)
            txt = response.text
            response_data = json.loads(txt)
            ciphertext = response_data['ciphertext']
            decrypted_response = encryption_agent.decrypt(ciphertext)
            if response.status_code == 200:
                logger.info(
                    f'EngineRoomFeature {main_3d_view} added successfully.')
                return Response({'message': f'{decrypted_response}'}, status=status.HTTP_201_CREATED)
            else:
                logger.error(
                    f'error in add EngineRoomFeature {main_3d_view}, error msg: {decrypted_response}')
                return Response({'error': decrypted_response}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return super().create(request, *args, **kwargs)


class AddDeviceAPIView(APIView):
    permission_classes = [
        permissions.IsAuthenticated | permissions.IsAdminUser]

    def post(self, request):
        try:
            name = request.data.get('name')
            serial_number = request.data.get('serial_number')
            installation_address = request.data.get('installation_address')
            engineroom_feature = request.data.get('engine_room_feature')
            location = request.data.get('location')
            organization = request.data.get('organization')
            # step = request.data.get('step')
            status = request.data.get('status')
            # rejection_note = request.data.get('rejection_note')
            created_by = request.data.get('created_by')
            lat_long = request.data.get('lat_long')
            details = request.data.get('details')
            serial_number_pattern = re.compile(
                r'^([0-9A-Fa-f]{4}\.){3}[0-9A-Fa-f]{4}$')
            if Device.objects.using('teska_server').filter(name=name).exists():
                return Response({'message': "already exist"}, status=409)

            elif not serial_number_pattern.match(serial_number):
                return Response({'error': "Invalid serial number format"}, status=400)
            else:
                engine_room_feature = EngineRoomFeature.objects.using('teska_server').get(main_3d_view = engineroom_feature)
                encryption_agent = DataEncryptionAgent()
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': f'Api-Key {settings.API_KEY}'
                }
                body = {
                    'name': name,
                    'serial_number': serial_number,
                    'installation_address': installation_address,
                    'engine_room_feature': engine_room_feature.id,
                    'location': location,
                    'organization': organization,
                    'step': 0,
                    'status': status,
                    'rejection_note': '',
                    'created_by': created_by,
                    'lat_long': lat_long,
                    'details': details,
                }

                body_json = json.dumps(body)
                encrypted_body = encryption_agent.encrypt(body_json)

                # Prepare encrypted data
                encrypted_data = {'ciphertext': encrypted_body}

                response = requests.post(
                    settings.ADD_DEVICES_URL, json=encrypted_data, headers=headers)

                txt = response.text
                response_data = json.loads(txt)
                ciphertext = response_data['ciphertext']
                decrypted_response = encryption_agent.decrypt(ciphertext)
                if response.status_code == 200:

                    ###################################
                    device = get_object_or_404(Device.objects.using(
                        'teska_server'), serial_number=serial_number)

                    device_id = device.id
                    location_public_info = locationPublicInfo.objects.create(
                        device=device_id, serial_number=serial_number, user=created_by)
                    installation_info = InstallationInfo.objects.create(
                        device=device_id, serial_number=serial_number, user=created_by)
                    engin_room_public_info = EnginRoomPublicInfo.objects.create(
                        device=device_id, serial_number=serial_number, user=created_by)
                    logger.info(
                        f'create a record in a 3 table(location public info, installation info, enginroom public info)for device {device.name}')
                    EventHistory.objects.create(title='اضافه شدن اطلاعات موتورخانه',
                                                text=f'اطلاعات محل نصب، اطلاعات دستگاه نصب شده و اطلاعات موتورخانه برای موتور خانه {device.name} توسط کاربر {request.user.username} با موفقیت ایجاد شد.', user=request.user.id, device=device_id)
                    ##################################

                    logger.info(
                        f'Device {name} added successfully.')
                    EventHistory.objects.create(title='اضافه شدن موتورخانه',
                                                text=f' موتور خانه {device.name} توسط کاربر {request.user.username} با موفقیت ایجاد شد.', user=request.user.id, device=device_id)
                    return Response({'message': f'{decrypted_response}'})
                else:
                    logger.error(
                        f'error in add Device {name}')
                    return Response({'error': decrypted_response})

        except Exception as e :
            return Response({'error': str(e)}, status=500)
class UpdateDeviceAPIView(APIView):
    permission_classes = [
        permissions.IsAuthenticated | permissions.IsAdminUser]

    def post(self, request):
        device_id = request.data.get('id')
        name = request.data.get('name')
        serial_number = request.data.get('serial_number')
        installation_address = request.data.get('installation_address')
        engineroom_feature = request.data.get('engine_room_feature')
        location = request.data.get('location')
        organization = request.data.get('organization')
        # step = request.data.get('step')
        status = request.data.get('status')
        rejection_note = request.data.get('rejection_note')
        created_by = request.data.get('created_by')
        lat_long = request.data.get('lat_long')
        # details = request.data.get('details')
        serial_number_pattern = re.compile(
            r'^([0-9A-Fa-f]{4}\.){3}[0-9A-Fa-f]{4}$')

        device = Device.objects.using('teska_server').get(id=device_id)

        if not serial_number_pattern.match(serial_number):
            return Response({'error': "Invalid serial number format"}, status=400)
        else:
            engine_room_feature = EngineRoomFeature.objects.using('teska_server').get(main_3d_view = engineroom_feature)
            encryption_agent = DataEncryptionAgent()
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Api-Key {settings.API_KEY}'
            }
            body = {
                'id': device_id,
                'name': name,
                'serial_number': serial_number,
                'installation_address': installation_address,
                'engine_room_feature': engine_room_feature.id,
                'location': location,
                'organization': organization,
                'step': device.step,
                'status': status,
                'rejection_note': rejection_note,
                'created_by': created_by,
                'lat_long': lat_long,
                'details': device.details,
            }

            body_json = json.dumps(body)
            encrypted_body = encryption_agent.encrypt(body_json)

            # Prepare encrypted data
            encrypted_data = {'ciphertext': encrypted_body}

            response = requests.put(
                settings.EDIT_DEVICES_URL, json=encrypted_data, headers=headers)

            txt = response.text
            response_data = json.loads(txt)
            ciphertext = response_data['ciphertext']
            decrypted_response = encryption_agent.decrypt(ciphertext)
            if response.status_code == 200:

                device = Device.objects.using('teska_server').get(id=device_id)

                location_public_info = locationPublicInfo.objects.get(
                    device=device.id)
                installation_info = InstallationInfo.objects.get(
                    device=device_id)
                engin_room_public_info = EnginRoomPublicInfo.objects.get(
                    device=device_id)
                location_public_info.serial_number = device.serial_number
                location_public_info.user = device.created_by
                location_public_info.save()

                installation_info.serial_number = device.serial_number
                installation_info.user = device.created_by
                installation_info.save()

                engin_room_public_info.serial_number = device.serial_number
                engin_room_public_info.user = device.created_by
                engin_room_public_info.save()

                logger.info(
                    f'create a record in a 3 table(location public info, installation info, enginroom public info)for device {name}')
                EventHistory.objects.create(title='بروزرسانی اطلاعات موتورخانه',
                                            text=f'اطلاعات محل نصب، اطلاعات دستگاه نصب شده و اطلاعات موتورخانه برای موتور خانه {name} توسط کاربر {request.user.username} با موفقیت بروزرسانی شد.', user=request.user.id, device=device_id)
                ##################################

                logger.info(
                    f'Device {name} updated successfully.')
                EventHistory.objects.create(title='بروزرسانی موتورخانه',
                                            text=f' موتور خانه {name} توسط کاربر {request.user.username} با موفقیت بروزرسانی شد.', user=request.user.id, device=device_id)
                return Response({'message': f'{decrypted_response}'})
            else:
                logger.error(
                    f'error in update Device {name}')
                return Response({'error': decrypted_response})


class CreateEngineroomInfoRecord(APIView):
    permission_classes = [
        permissions.IsAuthenticated | permissions.IsAdminUser]

    def post(self, request, *args, **kwargs):
        serial_number = request.data.get('serial_number')
        user_id = request.data.get('user')

        if not serial_number or not user_id:
            return Response({'error': 'Both serial_number and user_id are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:

            device = get_object_or_404(Device.objects.using(
                'teska_server'), serial_number=serial_number)

            device_id = device.id
            location_public_info = locationPublicInfo.objects.create(
                device=device_id, serial_number=serial_number, user=user_id)
            installation_info = InstallationInfo.objects.create(
                device=device_id, serial_number=serial_number, user=user_id)
            engin_room_public_info = EnginRoomPublicInfo.objects.create(
                device=device_id, serial_number=serial_number, user=user_id)
            logger.info(
                f'create a record in a 3 table(location public info, installation info, enginroom public info)for device {device.name}')
            EventHistory.objects.create(title='اضافه شده اطلاعات موتورخانه',
                                        text=f'اطلاعات محل نصب، اطلاعات دستگاه نصب شده و اطلاعات موتورخانه برای موتور خانه {device.name} توسط کاربر {request.user.username} با موفقیت ایجاد شد.', user=request.user.id, device=device_id)

            return Response(status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(
                f'in creation of 3 record for device an error occured. error {str(e)}')
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DeviceAPIView(viewsets.ViewSet):
    permission_classes = [
        permissions.IsAuthenticated | permissions.IsAdminUser]

    @action(detail=True, methods=['GET'])
    def get_option_for_insert(self, request):

        try:
            current_user = self.request.user
            device = Device.objects.using('teska_server').values_list('id', 'name')
            # print(device)
            device_queryset = get_object_by_user(current_user, device)
            # print(device_queryset)
            organization_queryset = Organization.objects.using(
                'teska_server').all()

            location_queryset = Location.objects.using(
                'teska_server').all()

            features_queryset = EngineRoomFeature.objects.using(
                'teska_server').all()

        #######################################################

            if current_user.is_superuser and current_user.is_staff:
                shouka_installers_queryset = User.objects.all().order_by('id')
            elif current_user.is_staff and not current_user.is_superuser:
                shouka_installers_queryset = User.objects.filter(
                    Q(profile__owner=current_user) | Q(profile__user=current_user)).order_by('id')
            else:
                shouka_installers_queryset = User.objects.filter(
                    profile__user=current_user)
        ################################################

            options = {}

            organizations = organization_queryset.values_list(
                'id', 'organization')
            administrations = organization_queryset.values_list(
                'id', 'administration')
            
            unique_administrations = {administration.strip() for _, administration in administrations}

            shouka_installers = shouka_installers_queryset.values_list(
                'id', 'username')

            locations = location_queryset.values_list('id', 'province', 'city')

            features = features_queryset.values_list('id', 'main_3d_view')

            options['organizations'] = [{'id': id, 'organization': organization}
                                        for id, organization in organizations]
            options['administration'] = [{'id': idx, 'administration': administration} for idx, administration in enumerate(unique_administrations)]

            options['locations'] = [{'id': id, 'location': (province, city)}
                                    for id, province, city in locations]

            options['features'] = [{'id': id, 'main_3d_view': main_3d_view}
                                   for id, main_3d_view in features]

            options['installers'] = [{'id': id, 'installer': username}
                                     for id, username in shouka_installers]

            options['devices'] = [{'id': id, 'name': name}
                                  for id, name in device_queryset]
        

            return Response(options)
        except Exception as e:
            logger.error(str(e))
            return Response({'error': str(e)})

    @action(detail=False, methods=['GET'])
    def get_object_count(self, request):

        object_count = {}

        device = Device.objects.using('teska_server')
        device = get_object_by_user(request.user, device)
        device_count = device.count()
        organization_count = Organization.objects.using('teska_server').count()
        location_count = Location.objects.using('teska_server').count()
        engineroom_feature_count = EngineRoomFeature.objects.using(
            'teska_server').count()

        object_count['device'] = device_count
        object_count['organization'] = organization_count
        object_count['location'] = location_count
        object_count['engineroom_feature'] = engineroom_feature_count

    # user = self.request.user
    #     if user.is_superuser and user.is_staff:
    #         count = Device.objects.count()
    #     elif user.is_staff and not user.is_superuser:
    #         count = Device.objects.filter(
    #             Q(creator=user) | Q(creator__profile__owner=user)).count()
    #     else:
    #         count = Device.objects.filter(created_by=1).count()

        return Response(object_count)

    @action(detail=True, methods=['POST'])
    def update_device_by_status(self, request):
        device_id = request.data.get('id')
        status = request.data.get('status')
        rejection_note = request.data.get('rejection_note')

        try:
            device = Device.objects.using('teska_server').get(pk=device_id)

            organization = Organization.objects.using('teska_server').get(
                organization=device.organization.organization)

            encryption_agent = DataEncryptionAgent()
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Api-Key {settings.API_KEY}'
            }
            body = {
                'id': device_id,
                'name': device.name,
                'serial_number': device.serial_number,
                'installation_address': device.installation_address,
                'engine_room_feature': device.engine_room_feature.id,
                'location': device.location.id,
                'organization': device.organization.id,
                'step': device.step,
                'status': status,
                'rejection_note': rejection_note,
                'created_by': device.created_by,
                'lat_long': device.lat_long,
                'details': device.details,
            }

            body_json = json.dumps(body)
            encrypted_body = encryption_agent.encrypt(body_json)

            # Prepare encrypted data
            encrypted_data = {'ciphertext': encrypted_body}

            response = requests.put(
                settings.EDIT_DEVICES_URL, json=encrypted_data, headers=headers)

            txt = response.text
            response_data = json.loads(txt)
            ciphertext = response_data['ciphertext']
            decrypted_response = encryption_agent.decrypt(ciphertext)
            logger.info(f'{device.name} updated successfully.')
            if response.status_code == 200:
                logger.info(f'{decrypted_response}')
                return Response({'message': f'{decrypted_response}'})
            else:
                logger.error(f'{decrypted_response}')
                return Response({'error': f'{decrypted_response}'})

        except Device.DoesNotExist:
            logger.error('Device not found.')
            return Response({'error': 'Device not found.'})

        except Exception as e:
            logger.error(str(e))
            return Response({'error': str(e)})

    @action(detail=False, methods=['GET'])
    def get_locations(self, request):
        queryset = Device.objects.using('teska_server').all()
        user = request.user
        queryset = get_object_by_user(user, queryset)
        installer = request.GET.get('installer')
        organization = request.GET.get('organization')
        administration = request.GET.get('administration')
        province = request.GET.get('province')
        city = request.GET.get('city')

        if installer:
            queryset = queryset.filter(created_by=installer)
        if organization:
            queryset = queryset.filter(organization__organization=organization)
        if administration:
            queryset = queryset.filter(
                organization__administration=administration)
        if province:
            queryset = queryset.filter(location__province=province)
        if city:
            queryset = queryset.filter(location__city=city)

        serializer = DeviceSerializer(queryset, many=True)
        serialized_data = serializer.data

        filter_locations = [
            {key: item[key] for key in ['id', 'name',
                                        'province', 'city', 'lat_long', 'creator']}
            for item in serialized_data
        ]
        logger.info("Filter locations loaded succesfully")
        return Response(filter_locations)

    @action(detail=True, methods=['POST'])
    def update_engineroom_details(self, request):
        device_id = request.data.get('id')
        details = request.data.get('details')

        try:
            device = Device.objects.using('teska_server').get(pk=device_id)
            device_status = get_device_status(device.status)
            encryption_agent = DataEncryptionAgent()
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Api-Key {settings.API_KEY}'
            }
            body = {
                'id': device_id,
                'name': device.name,
                'serial_number': device.serial_number,
                'installation_address': device.installation_address,
                'engine_room_feature': device.engine_room_feature.id,
                'location': device.location.id,
                'organization': device.organization.id,
                'step': device.step,
                'status': device_status,
                'rejection_note': device.rejection_note,
                'created_by': device.created_by,
                'lat_long': device.lat_long,
                'details': details,
            }

            body_json = json.dumps(body)
            encrypted_body = encryption_agent.encrypt(body_json)

            # Prepare encrypted data
            encrypted_data = {'ciphertext': encrypted_body}

            response = requests.put(
                settings.EDIT_DEVICES_URL, json=encrypted_data, headers=headers)

            txt = response.text
            response_data = json.loads(txt)
            ciphertext = response_data['ciphertext']
            decrypted_response = encryption_agent.decrypt(ciphertext)
            
            if response.status_code == 200:
                logger.info(f'{device.name} details updated successfully.')
                return Response({'message': f'{decrypted_response}'})
            else:
                logger.error(f'{decrypted_response}')
                return Response({'error': f'{decrypted_response}'})

        except Device.DoesNotExist:
            return Response({'error': 'Device not found.'})

        except Exception as e:
            logger.error(str(e))
            return Response({'error': str(e)})

    @action(detail=True, methods=['POST'])
    def update_engineroom_step(self, request):
        device_id = request.data.get('id')
        step = request.data.get('step')

        try:
            device = Device.objects.using('teska_server').get(pk=device_id)
            device_status = get_device_status(device.status)
            encryption_agent = DataEncryptionAgent()
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Api-Key {settings.API_KEY}'
            }
            body = {
                'id': device_id,
                'name': device.name,
                'serial_number': device.serial_number,
                'installation_address': device.installation_address,
                'engine_room_feature': device.engine_room_feature.id,
                'location': device.location.id,
                'organization': device.organization.id,
                'step': step,
                'status': device_status,
                'rejection_note': device.rejection_note,
                'created_by': device.created_by,
                'lat_long': device.lat_long,
                'details': device.details,
            }
            print('device status ', device_status, type(device_status))
            body_json = json.dumps(body)
            encrypted_body = encryption_agent.encrypt(body_json)

            # Prepare encrypted data
            encrypted_data = {'ciphertext': encrypted_body}

            response = requests.put(
                settings.EDIT_DEVICES_URL, json=encrypted_data, headers=headers)

            txt = response.text
            response_data = json.loads(txt)
            ciphertext = response_data['ciphertext']
            decrypted_response = encryption_agent.decrypt(ciphertext)
            
            if response.status_code == 200:
                logger.info(f'{device.name} step updated successfully.')
                return Response({'message': f'{decrypted_response}'})
            else:
                logger.info(f'{decrypted_response} step updated successfully.')
                return Response({'error': f'{decrypted_response}'})

        except Device.DoesNotExist:
            logger.error('Device not found.')
            return Response({'error': 'Device not found.'})

        except Exception as e:
            logger.error(str(e))
            return Response({'error': str(e)})
