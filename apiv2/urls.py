from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter


urlpatterns = [
    path('devices-list/',views.ListDevicesAPIView.as_view(), name='list-devices'),
    path('objects/<str:model_name>/',
         views.ListObjectsAPIView.as_view(), name='list-objects'),
    path('objects/<str:model_name>/<int:pk>/',
         views.RetrieveObjectsAPIView.as_view(), name='retrieve-object'),
    path('create-engineroom-info/',
         views.CreateEngineroomInfoRecord.as_view(), name='retrieve-object'),

    path('get_option_for_insert/', views.DeviceAPIView.as_view({'get': 'get_option_for_insert'}),
         name='get_option_for_insert'),
    path('get_object_count/', views.DeviceAPIView.as_view({'get': 'get_object_count'}),
         name='get_device_count'),

    path('get_locations/', views.DeviceAPIView.as_view({'get': 'get_locations'}),
         name='get_locations'),

    path('update_device_by_status/',
         views.DeviceAPIView.as_view({'post': 'update_device_by_status'})),

    path('update_engineroom_details/',
         views.DeviceAPIView.as_view({'post': 'update_engineroom_details'})),

    path('update_engineroom_step/',
         views.DeviceAPIView.as_view({'post': 'update_engineroom_step'})),
    path('objects/<str:model_name>/add/',
         views.CreateObjectApiView.as_view(), name='create--objects'),
    path('objects/<str:model_name>/edit/',
         views.UpdateObjectApiView.as_view(), name='update--objects'),
    path('device/add/',
         views.AddDeviceAPIView.as_view(), name='create-device'),

    path('device/edit/',
         views.UpdateDeviceAPIView.as_view(), name='update-device'),

]
