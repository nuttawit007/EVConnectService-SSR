from django.db import models
from core.models import Appointment as CoreAppointment
from core.models import Vehicle as CoreVehicle
from core.models import Review as CoreReview
from core.models import Profile as CoreProfile

class BookingClient(models.Model):
    class Meta:
        managed = False  # ไม่สร้างตารางในฐานข้อมูล
        default_permissions = ()  # ปิดการสร้าง permissions เริ่มต้น
        app_label = "client"
        permissions = [
            ("access_booking_page", "Can access client booking page"),
        ]

class AppointmentClient(CoreAppointment):
    class Meta:
        proxy = True
        app_label = "client"
        permissions = [
            ("access_appointment_page", "Can access client appointment page"),
        ]

class VehicleClient(CoreVehicle):
    class Meta:
        proxy = True
        app_label = "client"
        permissions = [
            ("access_vehicle_page", "Can access client vehicle page"),
        ]

class ReviewClient(CoreReview):
    class Meta:
        proxy = True
        app_label = "client"
        permissions = [
            ("access_review_page", "Can access client review page"),
        ]

class ProfileClient(CoreProfile):
    class Meta:
        proxy = True
        app_label = "client"
        permissions = [
            ("access_profile_page", "Can access client profile page"),
        ]
