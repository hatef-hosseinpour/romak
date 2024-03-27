from rest_framework.parsers import MultiPartParser
from rest_framework import status, authentication, permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from main.models import locationPublicInfo, EnginRoomPublicInfo, InstallationInfo, EnginRoomImage, EventHistory
from api.serializers import LocationPublicInfoSerializers, EnginroomPublicInfoSerializers, InstallationInfoSerializers, EnginroomImagesSerializers, EventHistorySerializer
from django.db.models import Q
from api.pagination import CustomEngineroomPagination
from rest_framework.decorators import action
import logging
from api.utils import convertToJalali
from users.models import Profile

logger = logging.getLogger(__name__)


class EnginroomPublicInfoViewSet(viewsets.ModelViewSet):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAdminUser |
                          permissions.IsAuthenticated]

    queryset = EnginRoomPublicInfo.objects.all()
    serializer_class = EnginroomPublicInfoSerializers
    pagination_class = CustomEngineroomPagination

    lookup_field = 'device'

    # def get_queryset(self):
    #     user = self.request.user

    #     if user.is_superuser and user.is_staff:
    #         return EnginRoomPublicInfo.objects.all()
    #     elif user.is_staff and not user.is_superuser:
    #         return EnginRoomPublicInfo.objects.filter(user__profile__owner=user)
    #     else:
    #         return EnginRoomPublicInfo.objects.filter(user=user)

    def get_object(self):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        filter_kwargs = {self.lookup_field: self.kwargs[self.lookup_field]}
        obj = queryset.get(**filter_kwargs)
        self.check_object_permissions(self.request, obj)
        return obj


class LocationPublicInfoViewSet(viewsets.ModelViewSet):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAdminUser |
                          permissions.IsAuthenticated]
    queryset = locationPublicInfo.objects.all()

    serializer_class = LocationPublicInfoSerializers
    # pagination_class = CustomEngineroomPagination

    lookup_field = 'device'

    # def get_queryset(self):
    #     user = self.request.user

    #     # if user.is_superuser and user.is_staff:
    #     #     return locationPublicInfo.objects.all()
    #     # elif user.is_staff and not user.is_superuser:
    #     #     return locationPublicInfo.objects.filter(user__profile__owner=user)
    #     # else:
    #     #     return locationPublicInfo.objects.filter(user=user)

    def get_object(self):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        filter_kwargs = {self.lookup_field: self.kwargs[self.lookup_field]}
        obj = queryset.get(**filter_kwargs)
        self.check_object_permissions(self.request, obj)
        return obj


class InstallationInfoViewSet(viewsets.ModelViewSet):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAdminUser |
                          permissions.IsAuthenticated]

    queryset = InstallationInfo.objects.all()
    serializer_class = InstallationInfoSerializers
    pagination_class = CustomEngineroomPagination

    lookup_field = 'device'

    # def get_queryset(self):
    #     user = self.request.user

    #     if user.is_superuser and user.is_staff:
    #         return InstallationInfo.objects.all()
    #     elif user.is_staff and not user.is_superuser:
    #         return InstallationInfo.objects.filter(user__profile__owner=user)
    #     else:
    #         return InstallationInfo.objects.filter(user=user)

    def get_object(self):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        filter_kwargs = {self.lookup_field: self.kwargs[self.lookup_field]}
        obj = queryset.get(**filter_kwargs)
        self.check_object_permissions(self.request, obj)
        return obj


class EnginroomImagesViewSet(viewsets.ModelViewSet):
    parser_classes = [MultiPartParser]
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAdminUser |
                          permissions.IsAuthenticated]

    queryset = EnginRoomImage.objects.all()
    serializer_class = EnginroomImagesSerializers
    # pagination_class = CustomEngineroomPagination

    def list(self, request, *args, **kwargs):
        enginroom_id = request.query_params.get('device')

        if enginroom_id is not None:
            queryset = EnginRoomImage.objects.filter(device=enginroom_id)
        else:
            queryset = EnginRoomImage.objects.all()

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        enginroom_images = serializer.save()

        logger.info(f'{len(enginroom_images)} uploaded.')

        return Response({'images_uploaded': len(enginroom_images)},
                        status=status.HTTP_201_CREATED)


class EventHistoryViewSet(viewsets.ModelViewSet):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAdminUser |
                          permissions.IsAuthenticated]

    queryset = EventHistory.objects.all()
    serializer_class = EventHistorySerializer
    pagination_class = CustomEngineroomPagination

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        user = request.user

        if user.is_superuser and user.is_staff:
            queryset = queryset.all().order_by('-id')
        elif user.is_staff and not user.is_superuser:
        
            users = Profile.objects.filter(owner=user)
            user_ids = [profile['id'] for profile in users.values('id')]
            queryset = queryset.filter(Q(user=user.id) | Q(user__in=user_ids)).order_by('-id')
        else:
            queryset = queryset.filter(user=user.id).order_by('-id')
        serializer = self.get_serializer(queryset, many=True)

        for entry in serializer.data:
            entry['timestamp'] = convertToJalali(entry['timestamp'])

        page = self.paginate_queryset(serializer.data)

        return self.get_paginated_response(page)

    # @action(detail=False, methods=['GET'])
    # def get_filter_option(self, request):
    #     user = request.user
    #     filter_option = {}

    #     if user.is_superuser and user.is_staff:
    #         queryset = Enginroom.objects.all()
    #     elif user.is_staff and not user.is_superuser:
    #         queryset = Enginroom.objects.filter(
    #             Q(creator=user) | Q(creator__profile__owner=user))
    #     else:
    #         queryset = Enginroom.objects.filter(creator=user)

    #     engineroom_name = queryset.values_list('enginroom_name', flat=True)
    #     engineroom_id = queryset.values_list('id', flat=True)

    #     filter_option['engineroom'] = list(zip(engineroom_id, engineroom_name))
    #     return Response(filter_option)
