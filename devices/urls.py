from django.urls import path 

from . import views

app_name = 'devices'

urlpatterns = [
    path('', views.deviceList, name='device-home'),
    path('addcam/', views.addCamera, name='add-cam'),
    path('edit_cam/<int:pk>/', views.editCam, name='edit-cam'),
    path('setcamstatus/', views.setCamStatus, name='setcamstatus'),
    path('setcamflash/', views.setCamFlash, name='setcamflash'),
    path('register/', views.registerDevice, name='register-device'),
]