from rest_framework.parsers import MultiPartParser
from rest_framework import status, authentication, permissions, viewsets
from rest_framework.response import Response
from main.models import Enginroom, locationPublicInfo, EnginRoomPublicInfo, InstallationInfo, EnginRoomImage
from api.serializers import EnginroomSerializers, LocationPublicInfoSerializers, EnginroomPublicInfoSerializers, InstallationInfoSerializers, EnginroomImagesSerializers
from django.db.models import Q


class EnginroomPublicInfoViewSet(viewsets.ModelViewSet):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAdminUser |
                          permissions.IsAuthenticated]

    queryset = EnginRoomPublicInfo.objects.all()
    serializer_class = EnginroomPublicInfoSerializers

    lookup_field = 'enginroom'

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser and user.is_staff:
            return EnginRoomPublicInfo.objects.all()
        elif user.is_staff and not user.is_superuser:
            return EnginRoomPublicInfo.objects.filter(user__profile__owner=user)
        else:
            return EnginRoomPublicInfo.objects.filter(user=user)

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

    lookup_field = 'enginroom'

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser and user.is_staff:
            return locationPublicInfo.objects.all()
        elif user.is_staff and not user.is_superuser:
            return locationPublicInfo.objects.filter(user__profile__owner=user)
        else:
            return locationPublicInfo.objects.filter(user=user)

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

    lookup_field = 'enginroom'

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser and user.is_staff:
            return InstallationInfo.objects.all()
        elif user.is_staff and not user.is_superuser:
            return InstallationInfo.objects.filter(user__profile__owner=user)
        else:
            return InstallationInfo.objects.filter(user=user)

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

    def list(self, request, *args, **kwargs):
        enginroom_id = request.query_params.get('enginroom')

        if enginroom_id is not None:
            queryset = EnginRoomImage.objects.filter(enginroom=enginroom_id)
        else:
            queryset = EnginRoomImage.objects.all()

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        enginroom_images = serializer.save()

        return Response({'images_uploaded': len(enginroom_images)},
                        status=status.HTTP_201_CREATED)
