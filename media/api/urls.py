from django.urls import include, path
from .ApiViews.usersApiView import *
from .ApiViews.enginroomApiView import *
from .ApiViews.mainApiView import *

from rest_framework import routers

router = routers.DefaultRouter()

router.register(r'users', UserViewSet, basename='users')
router.register(r'users-profile', UserProfileViewSet)
router.register(r'enginroom', EnginroomViewSet, basename='enginroom')
router.register(r'location-public-info', LocationPublicInfoViewSet)
router.register(r'enginroom-public-info', EnginroomPublicInfoViewSet)
router.register(r'installation-info', InstallationInfoViewSet)
router.register(r'enginroom-images', EnginroomImagesViewSet)
router.register(r'event-history', EventHistoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('users/routes', view=getUserRoutes, name='get-users-routes'),
    path('login-user/', view=LoginUserApiView.as_view(),
         name='login-user'),
    path('logout-user/', view=LogoutUserApiView.as_view(),
         name='logout-user'),
    path('profile/', view=UserProfileApiView.as_view(), name='user-profile'),


    path('device/<str:serial_number>/',
         view=EngineroomBySerialNumber.as_view(), name='device')

    #     path('users-list/', view=UsersListApiView.as_view(), name='users-list'),
]
