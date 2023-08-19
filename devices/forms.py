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


    

