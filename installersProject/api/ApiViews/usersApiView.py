from rest_framework.response import Response
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

            is_admin = user.is_superuser
            profile = user.profile
            phone_number = profile.phone_number
            csrf_token = get_token(request)
            username = user.get_username()

            request.session['user_id'] = user.id
            request.session['phone_number'] = phone_number
            request.session['is_admin'] = is_admin
            request.session['username'] = username
            # request.session.set_expiry(value)

            return Response({'session_id': request.session.session_key, 'user_id': user.id, 'username': username, 'phone_number': phone_number, 'is_admin': is_admin, 'csrf_token': csrf_token}, status=status.HTTP_200_OK)
        else:
            return Response({'session_id': request.session.session_key}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutUserApiView(APIView):

    def get(self, request):
        logout(request)

        return Response({'message': 'Logout'}, status=status.HTTP_200_OK)


class UserProfileApiView(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        user = request.user
        profile = user.profile
        serializer = UserListSerializer(profile, many=False)
        return Response(serializer.data)


class UsersListApiView(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        current_user = request.user

        users = User.objects.exclude(pk=current_user.pk)
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
                'phone_number': data['phone_number']
            }

            userList.append(user_data)
        return Response(userList)


class UserViewSet(viewsets.ModelViewSet):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserSerializers

    def perform_create(self, serializer):
        
        password = self.request.data.get('password')

        hashed_password = make_password(password)
        serializer.validated_data['password'] = hashed_password
        serializer.save()

    # def perform_update(self, serializer):
    #     password = self.request.data.get('password')
    #     if password:
    #         hashed_password = make_password(password)
    #         serializer.validated_data['password'] = hashed_password
    #     serializer.save()


class UserProfileViewSet(viewsets.ModelViewSet):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAdminUser]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializers

    # def perform_update(self, serializer):
    #     instance = self.get_object()
    #     profile_image_file = self.request.data.get(
    #         'profile_image', None)  # type: ignore
    #     # print('profile_image: ', profile_image_file)
    #     if profile_image_file == "":
    #         serializer.validated_data['profile_image'] = instance.profile_image
    #     else:
    #         serializer.validated_data['profile_image'] = Base64ImageField(
    #         ).to_internal_value(profile_image_file)
    #     serializer.save()
