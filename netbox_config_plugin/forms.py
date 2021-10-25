from django import forms
from utilities.forms import BootstrapMixin

from dcim.models import Device
from .models import ConfigJob

class ConfigJobForm(BootstrapMixin, forms.ModelForm):

    device = forms.ModelChoiceField(queryset=Device.objects.all())

    class Meta:
        model = ConfigJob
        fields = ["device"]
