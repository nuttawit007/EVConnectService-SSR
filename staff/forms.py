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
