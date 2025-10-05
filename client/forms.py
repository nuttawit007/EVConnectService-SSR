from django import forms
from django.forms import ModelForm
from client.models import *

# handle Validation error
from django.core.exceptions import ValidationError

# regular expression
import re 

class VehicleForm(ModelForm):
    class Meta:
        model = Car
        fields = ["license_plate", "brand", "model"]

        base_attrs = {
            'class': 'w-full px-6 py-4 bg-slate-700 text-slate-300 placeholder-slate-500 rounded-2xl focus:outline-none focus:ring-2 focus:ring-yellow-400 transition-all',
            'maxlength': 50,
        }

        widgets = {
            'license_plate': forms.TextInput(attrs={**base_attrs, 'placeholder': 'enter your license plate'}),
            'brand': forms.TextInput(attrs={**base_attrs, 'placeholder': 'enter your brand name'}),
            'model': forms.TextInput(attrs={**base_attrs, 'placeholder': 'enter your model name'}),
        }

    def clean_license_plate(self):
        license_plate = self.cleaned_data.get('license_plate')

        # Convert to uppercase for consistency
        license_plate = license_plate.upper()

        # Pattern 1: 'SS NNNN' (S=2 letters, N=1-4 digits, first digit not 0)
        pattern1 = r'^[ก-ฮ]{2} [1-9]\d{0,3}$'
        # Pattern 2: 'N SS NNNN' (N=1 digit, S=2 letters, N=1-4 digits, first digit not 0)
        pattern2 = r'^\d{1} [ก-ฮ]{2} [1-9]\d{0,3}$'

        if not (re.match(pattern1, license_plate) or re.match(pattern2, license_plate)):
            raise ValidationError(
                "Invalid license plate format."
            )

        # Check for duplicate license plate (case-insensitive)
        if Car.objects.filter(license_plate__iexact=license_plate).exists():
            raise ValidationError("This license plate already exists.")

        return license_plate
