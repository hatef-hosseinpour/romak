from django.urls import include, path
from .ApiViews.usersApiView import *
from .ApiViews.enginroomApiView import *
from .ApiViews.mainApiView import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'users-profile', UserProfileViewSet)
router.register(r'enginroom', EnginroomViewSet, basename='enginroom')
router.register(r'location-public-info', LocationPublicInfoViewSet)
router.register(r'enginroom-public-info', EnginroomPublicInfoViewSet)
router.register(r'installation-info', InstallationInfoViewSet)
router.register(r'enginroom-images', EnginroomImagesViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('users/routes', view=getUserRoutes, name='get-users-routes'),
    path('login-user/', view=LoginUserApiView.as_view(),
         name='login-user'),
    path('logout-user/', view=LogoutUserApiView.as_view(),
         name='logout-user'),
    path('profile/', view=UserProfileApiView.as_view(), name='user-profile'),

    path('users-list/', view=UsersListApiView.as_view(), name='users-list'),
]
