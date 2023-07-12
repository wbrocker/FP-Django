from django.db import models

class ImageDetection(models.Model):
    image = models.ImageField(upload_to='images/')
    cameraId = models.CharField(max_length=10, default='')
    analyzed = models.BooleanField(default=False)       # Check if Detection have been done
    detection_data = models.TextField(default='{}')     # Store the Tensorflow data as JSON
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
