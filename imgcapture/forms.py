from django import forms
from .models import ImageDetection

class ImageForm(forms.ModelForm):

    class Meta:
        model = ImageDetection
        fields = ['image', 'cameraId']
