from django import forms
from .models import AlarmConfig, DetectionObjects

class AlarmForm(forms.ModelForm):
    class Meta:
        model = AlarmConfig
        fields = "__all__"
        exclude = ['current_type']
