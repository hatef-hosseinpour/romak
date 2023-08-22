from django.urls import path
from . import views
from .FrontendViews.usersFrontendView import *
from .FrontendViews.organizationFrontendView import *
from .FrontendViews.enginroomPublicInfoFrontView import *
from .FrontendViews.locationPublicInfoFrontView import *
from .FrontendViews.mainFrontendView import *
urlpatterns = [
    path('', view=homePageFrontView, name='front-index'),
    path('create-installation/', view=installationFrontView,
         name='create-installation'),
    path('login/', view=loginUserFrontView, name='front-login'),
    path('profile/', view=userProfileFrontView, name='front-profile'),
    path('users-list/', view=usersListFrontView, name='front-users-list'),
    path('create-user/', view=createUserFrontView, name='front-create-user'),
    path('user-details/<int:pk>', view=userDetailsFrontView,
         name='front-user-details'),
    path('update-user/<int:pk>', view=updateUserFrontView,
         name='front-update-user'),
    path('delete-user/<int:pk>', view=deleteUserFrontView,
         name='front-delete-user'),




    # enginroom URLs

    path('enginroom-list/', view=enginroomListFrontView,
         name='front-enginroom-list'),
    path('create-enginroom/', view=createEnginroomFrontView,
         name='front-create-enginroom'),
    path('update-enginroom/<int:pk>', view=updateEnginroomFrontView,
         name='front-update-enginroom'),


    # Enginroom Public Info URLs

    path('enginroom-info-list/', view=enginroomPublicInfoListFrontView,
         name='front-enginroom-info-list'),

    path('enginroom-info-detail/<int:pk>', view=enginroomPublicInfoDetialFrontView,
         name='front-enginroom-info-detail'),

    path('create-enginroom-info/', view=createEnginroomPublicInfoFrontView,
         name='front-create-enginroom-info'),

    path('update-enginroom-info/<int:pk>', view=updateEnginroomPublicInfoFrontView,
         name='front-update-enginroom-info'),



    # Location public info
    path('location-public-info-list/', view=locationPublicInfoListFrontView,
         name='front-location-public-info-list'),

    path('create-location-public-info/', view=createLocationPublicInfoFrontView,
         name='front-create-location-public-info'),
]
