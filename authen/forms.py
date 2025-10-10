from django import forms

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from core.models import Profile

from django.core.exceptions import ValidationError
import re

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ("username", "password")

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"].strip().capitalize()
        user.last_name = self.cleaned_data["last_name"].strip().capitalize()
        if commit:
            user.save()
        return user

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


class ProfileForm(forms.ModelForm):
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
