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

        # ใช้ช่วง Unicode \u0E00-\u0E7F เพื่อครอบคลุมสระและเครื่องหมายต่าง ๆ ของภาษาไทย
        # อนุญาตตัวอักษรไทย (รวมสระ/วรรณยุกต์), ตัวเลข และช่องว่างภายในข้อความ
        if not re.match(r'^[\u0E00-\u0E7F0-9 ]+$', license_plate):
            raise ValidationError("License plate must contain only Thai characters and numbers.")

        # Normalize แบบไม่มีช่องว่าง เพื่อใช้ตรวจซ้ำ
        normalized_in = re.sub(r'\s+', '', license_plate).lower()

        qs = Vehicle.objects.all()
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        for v in qs:
            existing = (v.license_plate or '')
            normalized_existing = re.sub(r'\s+', '', existing).lower()
            if normalized_existing == normalized_in:
                raise ValidationError("This license plate already exists.")

        return license_plate

    def clean_brand(self):
            brand = self.cleaned_data.get('brand')
            # อนุญาติเฉพาะ อักษรอังกฤษ ตัวเลข และช่องว่าง
            if not re.match(r'^[a-zA-Z0-9 ]+$', brand):
                raise ValidationError("Brand must contain only English letters, numbers.")

            return brand.capitalize()

    def clean_model(self):
            model = self.cleaned_data.get('model')
            # อนุญาติเฉพาะ อักษรอังกฤษ ตัวเลข และช่องว่าง
            if not re.match(r'^[a-zA-Z0-9 ]+$', model):
                raise ValidationError("Model must contain only English letters, numbers.")

            return model.capitalize()

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
