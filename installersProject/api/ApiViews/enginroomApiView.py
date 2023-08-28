from rest_framework import status, authentication, permissions, viewsets
from rest_framework.response import Response
from main.models import Enginroom, locationPublicInfo
from api.serializers import EnginroomSerializers


class EnginroomViewSet(viewsets.ModelViewSet):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAdminUser | permissions.IsAuthenticated]
    serializer_class = EnginroomSerializers

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return Enginroom.objects.all()
        else:
            return Enginroom.objects.filter(creator=user)
