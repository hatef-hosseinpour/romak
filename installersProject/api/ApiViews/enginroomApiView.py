from rest_framework import status, authentication, permissions, viewsets
from rest_framework.response import Response
from main.models import Enginroom, locationPublicInfo
from api.serializers import EnginroomSerializers
from django.contrib.auth.models import User


class EnginroomViewSet(viewsets.ModelViewSet):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAdminUser |
                          permissions.IsAuthenticated]
    serializer_class = EnginroomSerializers

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser and user.is_staff:
            return Enginroom.objects.all()
        elif user.is_staff and not user.is_superuser:
            return Enginroom.objects.filter(creator__profile__owner=user)
        else:
            return Enginroom.objects.filter(creator=user)
        
    def create(self, request, *args, **kwargs):
        enginroom_name = request.data.get('enginroom_name')

        # Check if an Enginroom with the same name already exists
        existing_enginroom = Enginroom.objects.filter(enginroom_name=enginroom_name).exists()
        
        if existing_enginroom:
            return Response({'detail': 'already exists'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
