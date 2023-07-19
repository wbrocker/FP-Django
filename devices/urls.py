from django.urls import path 

from . import views

app_name = 'devices'

urlpatterns = [
    path('', views.deviceList, name='device-home'),
    path('addcam/', views.addCamera, name='add-cam'),
    path('adddevice/', views.AddDevice, name='add-device'),
    path('edit_cam/<int:pk>/', views.editCam, name='edit-cam'),
    path('setcamstatus/', views.setCamStatus, name='setcamstatus'),
    path('setcamflash/', views.setCamFlash, name='setcamflash'),
    path('register/', views.registerDevice, name='register-device'),
    path('locations/', views.LocationList, name='locations'),
    path('addlocation/', views.AddLocation, name='add-loc'),
    path('editlocation/<int:pk>/', views.EditLocation, name='edit-loc'),
    path('delete/<int:pk>/', views.DeleteLocation, name='del-loc'),
]