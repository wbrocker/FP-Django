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
        exclude = ['type', 'firmware', 'status', 'data']
        # readonly_fields = ('type', 'ip',)

    # picInterval = forms.IntegerField(label='Picture Interval', required=True)
    # flash = forms.BooleanField(label='Flash', required=True)
    
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    #     self.fields['type'].widget.attrs['readonly'] = True
    #     self.fields['ip'].widget.attrs['readonly'] = True

class LocationForm(forms.ModelForm):

    class Meta:
        model = Locations
        fields = "__all__"

