from django import forms
from .models import Locations, ActiveDevices

class DeviceForm(forms.ModelForm):
    # json_data = CustomJSON(allowed_keys=['flash', 'picInterval'])
    class Meta:
        model = ActiveDevices
        fields = "__all__"
        exclude = ['type', 'firmware', 'status', 'data']

    widgets = {
        'name': forms.TextInput(attrs={'class': 'form-control'}),
        'description': forms.TextInput(attrs={'class': 'form-control'}),
    }
        # readonly_fields = ('type', 'ip',)

class LocationForm(forms.ModelForm):

    class Meta:
        model = Locations
        fields = "__all__"

class PicIntervalForm(forms.Form):
    picInterval = forms.IntegerField(label='Picture Interval')


    

