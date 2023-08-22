from rest_framework.parsers import MultiPartParser
from rest_framework import status, authentication, permissions, viewsets
from rest_framework.response import Response
from main.models import Enginroom, locationPublicInfo, EnginRoomPublicInfo, InstallationInfo, EnginRoomImage
from api.serializers import EnginroomSerializers, LocationPublicInfoSerializers, EnginroomPublicInfoSerializers, InstallationInfoSerializers, EnginroomImagesSerializers


class EnginroomPublicInfoViewSet(viewsets.ModelViewSet):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAdminUser]

    queryset = EnginRoomPublicInfo.objects.all()
    serializer_class = EnginroomPublicInfoSerializers

    lookup_field = 'enginroom'

    def get_object(self):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        filter_kwargs = {self.lookup_field: self.kwargs[self.lookup_field]}
        obj = queryset.get(**filter_kwargs)
        self.check_object_permissions(self.request, obj)
        return obj


class LocationPublicInfoViewSet(viewsets.ModelViewSet):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAdminUser]
    queryset = locationPublicInfo.objects.all()

    serializer_class = LocationPublicInfoSerializers

    lookup_field = 'enginroom'

    def get_object(self):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        filter_kwargs = {self.lookup_field: self.kwargs[self.lookup_field]}
        obj = queryset.get(**filter_kwargs)
        self.check_object_permissions(self.request, obj)
        return obj


class InstallationInfoViewSet(viewsets.ModelViewSet):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAdminUser]

    queryset = InstallationInfo.objects.all()
    serializer_class = InstallationInfoSerializers

    lookup_field = 'enginroom'

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
    permission_classes = [permissions.IsAdminUser]

    queryset = EnginRoomImage.objects.all()
    serializer_class = EnginroomImagesSerializers

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        enginroom_images = serializer.save()

        return Response({'images_uploaded': len(enginroom_images)},
                        status=status.HTTP_201_CREATED)
    # lookup_field = 'enginroom'

    # def get_object(self):
    #     queryset = self.get_queryset()
    #     queryset = self.filter_queryset(queryset)
    #     filter_kwargs = {self.lookup_field: self.kwargs[self.lookup_field]}
    #     obj = queryset.get(**filter_kwargs)
    #     self.check_object_permissions(self.request, obj)
    #     return obj
