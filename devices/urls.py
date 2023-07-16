from django.urls import path 

from . import views

app_name = 'devices'

urlpatterns = [
    path('', views.deviceList, name='device-home'),
    path('addcam/', views.addCamera, name='add-cam'),
]