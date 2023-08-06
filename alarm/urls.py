from django.urls import path

from . import views

app_name = 'alarm'

urlpatterns = [
    path('changestatus/', views.ChangeAlarmStatus, name='alarm-status'),
    path('config/', views.AlarmConfigView, name='alarm-config'),
]