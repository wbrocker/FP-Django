from django.urls import path

from .views import *
from . import views

app_name = 'imgcapture'

urlpatterns = [
    path('upload/', upload_image_view, name='upload_image'),
    path('delete/<int:pk>', views.delete_image, name='delete'),
    path('success', success, name='success'),
]