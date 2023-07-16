from django import forms
from .models import ActiveCamera

class ActiveCameraForm(forms.ModelForm):

    class Meta:
        model = ActiveCamera
        fields = "__all__"
        exclude = ["device_firmware"]