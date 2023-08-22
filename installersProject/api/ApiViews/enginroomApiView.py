from rest_framework import status, authentication, permissions, viewsets
from rest_framework.response import Response
from main.models import Enginroom, locationPublicInfo
from api.serializers import EnginroomSerializers, LocationPublicInfoSerializers



class EnginroomViewSet(viewsets.ModelViewSet):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAdminUser]

    queryset = Enginroom.objects.all()
    serializer_class = EnginroomSerializers



