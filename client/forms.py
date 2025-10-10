from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm

import re

from core.models import Appointment, Review, Vehicle, User, Profile

class VehicleForm(ModelForm):
    class Meta:
        model = Vehicle
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

        # ตรวจสอบทะเบียนซ้ำ (ยกเว้นทะเบียนของ instance เดิม)
        qs = Vehicle.objects.filter(license_plate__iexact=license_plate)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError("This license plate already exists.")

        return license_plate

class BookingForm(ModelForm):
    class Meta:
        model = Appointment
        fields = ["vehicle", "service_types", "description", "date", "time"]

        base_attrs = {
            'class': 'w-full px-6 py-4 bg-slate-700 text-slate-300 placeholder-slate-500 rounded-2xl focus:outline-none focus:ring-2 focus:ring-yellow-400 transition-all',
        }

        widgets = {
            'vehicle': forms.Select(attrs={**base_attrs}),
            'service_types': forms.SelectMultiple(attrs={**base_attrs, 'size': 5}),
            'description': forms.Textarea(attrs={**base_attrs, 'placeholder': 'enter description (optional)', 'rows': 4}),
            'date': forms.DateInput(attrs={**base_attrs, 'type': 'date'}),
            'time': forms.TimeInput(attrs={**base_attrs, 'type': 'time'}),
        }

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ["score", "comment"]

        base_attrs = {
            'class': 'w-full px-6 py-4 bg-slate-700 text-slate-300 placeholder-slate-500 rounded-2xl focus:outline-none focus:ring-2 focus:ring-yellow-400 transition-all',
        }

        widgets = {
            'score': forms.NumberInput(attrs={**base_attrs, 'placeholder': 'enter score (1-5)', 'min': 1, 'max': 5}),
            'comment': forms.Textarea(attrs={**base_attrs, 'placeholder': 'enter comment (optional)', 'rows': 4}),
        }

class UserForm(UserChangeForm):
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]

        base_attrs = {
            'class': 'w-full px-6 py-4 bg-slate-700 text-slate-300 placeholder-slate-500 rounded-2xl focus:outline-none focus:ring-2 focus:ring-yellow-400 transition-all',
            'maxlength': 50,
        }

        widgets = {
            'username': forms.TextInput(attrs={**base_attrs, 'placeholder': 'enter your username'}),
            'email': forms.EmailInput(attrs={**base_attrs, 'placeholder': 'enter your email'}),
            'first_name': forms.TextInput(attrs={**base_attrs, 'placeholder': 'enter your first name'}),
            'last_name': forms.TextInput(attrs={**base_attrs, 'placeholder': 'enter your last name'}),
        }

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')

        if not first_name or str(first_name).strip() == "":
            raise ValidationError("First name is required.")

        # ต้องเป็นอักษรเท่านั้น และสามาระเป็นค่าว่างได้
        if first_name and not first_name.isalpha():
            raise ValidationError("First name must contain only letters.")
        return first_name.capitalize()

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')

        if not last_name or str(last_name).strip() == "":
            raise ValidationError("Last name is required.")

        # ต้องเป็นอักษรเท่านั้น และสามาระเป็นค่าว่างได้
        if last_name and not last_name.isalpha():
            raise ValidationError("Last name must contain only letters.")
        return last_name.capitalize()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email or str(email).strip() == "":
            raise ValidationError("Email is required.")
        return email


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ["phone_number"]

    base_attrs = {
        'class': 'w-full px-6 py-4 bg-slate-700 text-slate-300 placeholder-slate-500 rounded-2xl focus:outline-none focus:ring-2 focus:ring-yellow-400 transition-all',
        'maxlength': 15,
        'placeholder': 'enter your phone number',
    }

    phone_number = forms.CharField(widget=forms.TextInput(attrs=base_attrs))

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')

        if not phone_number or str(phone_number).strip() == "":
            raise ValidationError("Phone number is required.")

        # ต้องการแค่ pattern  0XXXXXXXXX นี้เท่านั้น
        pattern = r'^0\d{9}$'
        if not re.match(pattern, phone_number):
            raise ValidationError("Invalid phone number format.")

        qs = Profile.objects.filter(phone_number=phone_number)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError("This phone number already exists.")

        return phone_number

class PasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ["old_password", "new_password1", "new_password2"]

    base_attrs = {
        'class': 'w-full px-6 py-4 bg-slate-700 text-slate-300 placeholder-slate-500 rounded-2xl focus:outline-none focus:ring-2 focus:ring-yellow-400 transition-all',
        'maxlength': 128,
    }

    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={**base_attrs, 'placeholder': 'enter your old password'})
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={**base_attrs, 'placeholder': 'enter your new password'})
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={**base_attrs, 'placeholder': 'confirm your new password'})
    )
