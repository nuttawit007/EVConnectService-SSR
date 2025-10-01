from django.contrib.auth.models import AbstractUser
from django.db import models


class User(models.Model):
    class Role(models.Choices):
        CUSTOMER = "CUSTOMER"
        STAFF = "STAFF"
    username = models.CharField(max_length=225, unique=True)
    password = models.CharField(max_length=225)
    fname = models.CharField(max_length=225)
    lname = models.CharField(max_length=225)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.CUSTOMER)

    def __str__(self):
        return f"User : {self.username} ({self.role})"


class Car(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cars")
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    license_plate = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"Car : {self.brand} {self.model} ({self.license_plate})"


class ServiceType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return f"Service name : {self.name}"


class Appointment(models.Model):
    class Status(models.Choices):
        PENDING = "PENDING"
        IN_PROGRESS = "IN-PROGRESS"
        DONE = "DONE"
        REJECT = "REJECT"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="appointments")
    car = models.OneToOneField(Car, on_delete=models.CASCADE, related_name="appointment")
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    service_types = models.ManyToManyField(ServiceType, related_name='services')

    def __str__(self):
        return f"Appointment id : #{self.pk}"


class Rating(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name="rating")
    score = models.IntegerField()
    comment = models.TextField()

    def __str__(self) -> str:
        return f"Rating id : #{self.pk} - {self.score}"
