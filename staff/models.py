from django.db import models
from core.models import Appointment as CoreAppointment
from core.models import Vehicle as CoreVehicle
from core.models import Review as CoreReview

class StaffPortal(models.Model):
    class Meta:
        managed = False  # ไม่สร้างตารางในฐานข้อมูล
        default_permissions = ()  # ปิดการสร้าง permissions เริ่มต้น
        app_label = "staff"
        permissions = [
            ("access_dashboard", "Can access staff dashboard"),
        ]

class AppointmentStaff(CoreAppointment):
    class Meta:
        proxy = True
        app_label = "staff"
        permissions = [
            ("access_appointment_page", "Can access staff appointment page"),
        ]

class VehicleStaff(CoreVehicle):
    class Meta:
        proxy = True
        app_label = "staff"
        permissions = [
            ("access_vehicle_page", "Can access staff vehicle page"),
        ]

class ReviewStaff(CoreReview):
    class Meta:
        proxy = True
        app_label = "staff"
        permissions = [
            ("access_review_page", "Can access staff review page"),
        ]
