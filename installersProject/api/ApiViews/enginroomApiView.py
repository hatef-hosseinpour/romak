from rest_framework import status, authentication, permissions, viewsets
from rest_framework.response import Response
from main.models import Enginroom, locationPublicInfo
from api.serializers import EnginroomSerializers
from django.contrib.auth.models import User
from django.db.models import Q, F
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from api.pagination import CustomEngineroomPagination


class EnginroomViewSet(viewsets.ModelViewSet):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAdminUser |
                          permissions.IsAuthenticated]
    serializer_class = EnginroomSerializers

    pagination_class = CustomEngineroomPagination

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser and user.is_staff:
            queryset = Enginroom.objects.all()
        elif user.is_staff and not user.is_superuser:
            queryset = Enginroom.objects.filter(
                Q(creator=user) | Q(creator__profile__owner=user))
        else:
            queryset = Enginroom.objects.filter(creator=user)

        return queryset

    def create(self, request, *args, **kwargs):
        enginroom_name = request.data.get('enginroom_name')

        # Check if an Enginroom with the same name already exists
        existing_enginroom = Enginroom.objects.filter(
            enginroom_name=enginroom_name).exists()

        if existing_enginroom:
            return Response({'detail': 'already exists'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, methods=['GET'])
    def get_enginroom_count(self, request):
        user = self.request.user

        if user.is_superuser and user.is_staff:
            count = Enginroom.objects.count()
        elif user.is_staff and not user.is_superuser:
            count = Enginroom.objects.filter(
                Q(creator=user) | Q(creator__profile__owner=user)).count()
        else:
            count = Enginroom.objects.filter(creator=user).count()

        return Response({'count': count})

    # @action(detail=False, methods=['GET'])
    # def filter_enginrooms(self, request):
    #     value = request.query_params.get('value', None)
    #     user = self.request.user

    #     if user.is_superuser and user.is_staff:
    #         queryset = Enginroom.objects.all()
    #     elif user.is_staff and not user.is_superuser:
    #         queryset = Enginroom.objects.filter(
    #         Q(creator=user) | Q(creator__profile__owner=user))
    #     else:
    #         queryset = Enginroom.objects.filter(creator=user)

    #     if value:
    #         # Use Q objects to filter each field for the specified value
    #         query = Q()
    #         query |= Q(enginroom_name__icontains=value)
    #         query |= Q(organization__icontains=value)
    #         query |= Q(administration__icontains=value)
    #         # Add more fields as needed

    #         queryset = queryset.filter(query)

    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def get_filter_option(self, request):
        user = request.user
        filter_option = {}

        if user.is_superuser and user.is_staff:
            queryset = Enginroom.objects.all()
        elif user.is_staff and not user.is_superuser:
            queryset = Enginroom.objects.filter(
                Q(creator=user) | Q(creator__profile__owner=user))
        else:
            queryset = Enginroom.objects.filter(creator=user)

        installers = queryset.values_list('creator__username', flat=True)
        organizations = queryset.values_list('organization', flat=True)
        administrations = queryset.values_list('administration', flat=True)
        province = queryset.values_list(
            'locationpublicinfo__province', flat=True)
        city = queryset.values_list('locationpublicinfo__city', flat=True)
        filter_option['installers'] = list(set(installers))
        filter_option['organizations'] = list(set(organizations))
        filter_option['administrations'] = list(set(administrations))
        filter_option['province'] = list(set(province))
        filter_option['city'] = list(set(city))

        # if filter_option['city'] in ("", None):
        #    filter_option['city'] = "no-city"

        # if filter_option['city'] == "no-city":

        #     queryset = queryset.filter(Q(locationpublicinfo__city__isnull=True) | Q(locationpublicinfo__city=""))
        # else:

        #     queryset = queryset.filter(locationpublicinfo__city=filter_option['city'])

        return Response(filter_option)

    # @action(detail=False, methods=['GET'])
    # def get_enginerooms_by_user(self, request):
    #     user = request.user

    #     engineroom_list = Enginroom.objects.filter(creator=user)

    #     serializer = EnginroomSerializers(engineroom_list, many=True)

    #     return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def get_locations(self, request):
        user = request.user
        filter_locations = []

        if user.is_superuser and user.is_staff:
            queryset = Enginroom.objects.all()
        elif user.is_staff and not user.is_superuser:
            queryset = Enginroom.objects.filter(
                Q(creator=user) | Q(creator__profile__owner=user))
        else:
            queryset = Enginroom.objects.filter(creator=user)

        installer = request.GET.get('installer')
        organization = request.GET.get('organization')
        administration = request.GET.get('administration')
        province = request.GET.get('province')
        city = request.GET.get('city')

        if installer:
            queryset = queryset.filter(creator__username=installer)
        if organization:
            queryset = queryset.filter(organization=organization)
        if administration:
            queryset = queryset.filter(administration=administration)
        if province:
            queryset = queryset.filter(locationpublicinfo__province=province)
        if city:
            queryset = queryset.filter(locationpublicinfo__city=city)

        enginerooms = queryset.values('id', 'enginroom_name', province=F('locationpublicinfo__province'), city=F(
            'locationpublicinfo__city'), location=F('locationpublicinfo__location'))

        for engineroom in enginerooms:
            filter_locations.append(engineroom)

        return Response(filter_locations)
