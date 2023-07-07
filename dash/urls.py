from django.urls import path

from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name='dash'),
    path('images/', views.imageList, name='image-list'),
]