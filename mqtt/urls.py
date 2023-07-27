from django.urls import path
from . import views

app_name = 'mqtt'

urlpatterns = [
    path('publish', views.publish_message, name='publish'),
]