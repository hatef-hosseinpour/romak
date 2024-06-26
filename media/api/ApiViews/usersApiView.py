from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView
from rest_framework import status, authentication, permissions, viewsets
from users.models import Profile
from api.serializers import ProfileSerializers, UserSerializers, UserListSerializer
from django.middleware.csrf import get_token
from api.utils import Base64ImageField
from rest_framework import serializers
from api.pagination import CustomUserPagination
import logging

logger = logging.getLogger(__name__)
@api_view(['GET'])
def getUserRoutes(request):

    routes = [
        {'POST': '/api/users/login-user'},
        {'GET': '/api/users/logout-user'},
        {'GET': '/api/users/profile'},
    ]
    return Response(routes)


class LoginUserApiView(APIView):

    authentication_classes = [authentication.SessionAuthentication]

    def post(self, request):
        username = request.data['username'].lower()
        password = request.data['password']

        user = authenticate(username=username, password=password)
        if user is not None:

            login(request, user)

            is_admin = user.is_superuser  # Corrected attribute name
            is_staff = user.is_staff and not is_admin  # Corrected attribute name
            profile = user.profile
            phone_number = profile.phone_number
            csrf_token = get_token(request)
            # username = username

            request.session['user_id'] = user.id
            request.session['phone_number'] = phone_number
            request.session['is_admin'] = is_admin
            request.session['is_staff'] = is_staff
            request.session['username'] = username
            # request.session.set_expiry(value)
            logger.info(f'{username} logged in successfully.')
            return Response({'session_id': request.session.session_key, 'user_id': user.id, 'username': username, 'phone_number': phone_number, 'is_admin': is_admin, 'is_staff': is_staff, 'csrf_token': csrf_token}, status=status.HTTP_200_OK)
        
        else:
            logger.error(f'{username} logged in unsuccessfully.')
            return Response({'session_id': request.session.session_key}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutUserApiView(APIView):

    def get(self, request):
        logger.info(f'{str(request.user)} logged out successfully.')
        logout(request)

        return Response({'message': 'Logout'}, status=status.HTTP_200_OK)


class UserProfileApiView(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAdminUser |
                          permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        profile = user.profile
        serializer = UserListSerializer(profile, many=False)
        return Response(serializer.data)


class UsersListApiView(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAdminUser |
                          permissions.IsAuthenticated]
    

    def get(self, request):
        current_user = request.user
        profile = current_user.profile
        if current_user.is_superuser and current_user.is_staff:
            users = User.objects.all()
        elif current_user.is_staff and not current_user.is_superuser:
            users = User.objects.filter(profile__owner=current_user)
        else:
            users = User.objects.none()

        users_profile = Profile.objects.filter(user__in=users)
        serializer = UserListSerializer(users_profile, many=True)

        userList = []
        for data in serializer.data:

            user_data = {
                'id': data['user']['id'],
                'is_staff': data['user']['is_staff'],
                'is_superuser': data['user']['is_superuser'],
                'first_name': data['user']['first_name'],
                'last_name': data['user']['last_name'],
                'username': data['user']['username'],
                'email': data['user']['email'],
                'is_active': data['user']['is_active'],
                'profile_image': data['profile_image'],
                'phone_number': data['phone_number'],
                'owner': data['owner']
            }

            userList.append(user_data)
        return Response(userList)


class UserViewSet(viewsets.ModelViewSet):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAdminUser |
                          permissions.IsAuthenticated]
    # queryset = User.objects.all()
    serializer_class = UserSerializers
    pagination_class = CustomUserPagination

    def get_queryset(self):
        current_user = self.request.user
        profile = current_user.profile
        if current_user.is_superuser and current_user.is_staff:
            queryset = User.objects.all().order_by('id')
        elif current_user.is_staff and not current_user.is_superuser:
            queryset = User.objects.filter(Q(profile__owner=current_user) | Q(profile__user = current_user)).order_by('id')
        else:
            queryset = User.objects.filter(profile__user = current_user)
        
        return queryset

    def perform_create(self, serializer):

        password = self.request.data.get('password')

        hashed_password = make_password(password)
        serializer.validated_data['password'] = hashed_password
        user = serializer.save()

        # Return the user ID in the response
        data = {'user_id': user.id}
        logger.info(f'Password of {user} hashed')
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def reset_password(self, request, pk=None):
        user = self.get_object()
        new_password = request.data.get('new_password')

        if new_password:
            hashed_password = make_password(new_password)
            user.password = hashed_password
            user.save()
            logger.info(f'{user} password changed succesfully.')
            return Response({'message': 'success'}, status=status.HTTP_200_OK)
        else:
            logger.error(f'{user} password changed failed.')
            return Response({'error': 'fail'}, status=status.HTTP_400_BAD_REQUEST)

class UserProfileViewSet(viewsets.ModelViewSet):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAdminUser |
                          permissions.IsAuthenticated]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializers
    # pagination_class = CustomUserPagination
