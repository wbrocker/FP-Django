from django import forms
from .models import ActiveCamera, Locations

class ActiveCameraForm(forms.ModelForm):

    class Meta:
        model = ActiveCamera
        fields = "__all__"
        exclude = ["device_firmware"]

class LocationForm(forms.ModelForm):

    class Meta:
        model = Locations
        fields = "__all__"

