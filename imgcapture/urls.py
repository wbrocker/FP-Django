from django.urls import path

from .views import *
from . import views

app_name = 'imgcapture'

urlpatterns = [
    path('upload/', upload_image_view, name='upload_image'),        # Upload images
    path('delete/<int:pk>', views.delete_image, name='delete'),     # Delete Images
    path('analyze/<int:pk>', views.re_analyze, name='analyze'),     # Re-analyze images
    path('dnd/<int:pk>/', views.dnd, name='dnd'),                   # Setting the Do-Not-Delete.
    path('delete_all/', views.delete_all, name='del_all'),          # Delete All images
    path('success', success, name='success'),                       # Success Endpoint
]