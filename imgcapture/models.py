from django.db import models

class ImageDetection(models.Model):
    image = models.ImageField(upload_to='images/')
    cameraId = models.CharField(max_length=10, default='')
    analyzed = models.BooleanField(default=False)       # Check if Detection have been done
    detection_data = models.TextField(default='{}')     # Store the Tensorflow data as JSON
    dnd = models.BooleanField(default=False)            # Do Not Delete Flag
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"CameraId: { self.cameraId} taken { self.created}"