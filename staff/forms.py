from django import forms

from core.models import Appointment


class AppointmentStatusForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ["status"]
        widgets = {
            "status": forms.RadioSelect(
                choices=Appointment.Status.choices,
                attrs={"class": "hidden"},
            )
        }

    def clean_status(self):
        status = self.cleaned_data.get("status")
        if status not in dict(Appointment.Status.choices):
            raise forms.ValidationError("Invalid status selection.")
        return status

class EmailForm(forms.Form):
    base_attrs = {
        'class': 'w-full px-6 py-3 bg-slate-700 text-slate-300 placeholder-slate-500 rounded-xl focus:outline-none focus:ring-2 focus:ring-yellow-400 transition-all',
        'maxlength': 255,
    }

    subject = forms.CharField(max_length=255, widget=forms.TextInput(attrs={
        **base_attrs,
        'placeholder': 'Subject'
    }))
    message = forms.CharField(widget=forms.Textarea(attrs={
        **base_attrs,
        'placeholder': 'Your message here...',
        'rows': 6
    }))
