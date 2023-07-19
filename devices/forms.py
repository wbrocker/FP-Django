from django import forms
from .models import ActiveCamera, Locations, ActiveDevices

class ActiveCameraForm(forms.ModelForm):

    class Meta:
        model = ActiveCamera
        fields = "__all__"
        exclude = ["device_firmware"]

class DeviceForm(forms.ModelForm):

    class Meta:
        model = ActiveDevices
        fields = "__all__"
        exclude = ["firmware"]

class LocationForm(forms.ModelForm):

    class Meta:
        model = Locations
        fields = "__all__"

