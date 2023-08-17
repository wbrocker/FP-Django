from django.urls import path

from . import views

app_name = 'alarm'

urlpatterns = [
    path('changestatus/', views.ChangeAlarmStatus, name='alarm-status'),
    path('config/', views.AlarmConfigView, name='alarm-config'),
    path('objects/', views.AlarmDetectionObjects, name='alarm-detection'),
    path('setobjects/', views.ToggleObject, name='alarm-obj-toggle'),
    path('ack/', views.AckAlarm, name='ack-alarm'),
]