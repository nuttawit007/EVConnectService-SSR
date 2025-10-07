from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    phone_number = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return f"User : {self.user.username}"


class Vehicle(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="vehicles",
        default=1,
    )
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    license_plate = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"Vehicle : {self.brand} {self.model} ({self.license_plate})"

class ServiceType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Service name : {self.name}"


class Appointment(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        IN_PROGRESS = "IN-PROGRESS", "In progress"
        DONE = "DONE", "Done"
        REJECT = "REJECT", "Reject"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="appointments")
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="appointments", default=1)
    description = models.TextField(blank=True, null=True)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    service_types = models.ManyToManyField(ServiceType, related_name="services")

    def __str__(self):
        return f"Appointment id : #{self.pk}"

    def display_date_time(self):
        date = self.date.strftime("%d/%m/%Y")
        time = self.time.strftime("%H:%M")
        return f"{date} - {time}"


class Review(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name="review")
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return f"Review id : #{self.pk} - {self.score}"
