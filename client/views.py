from django.shortcuts import render, redirect
from django.views import View
from client.models import *

from client.forms import VehicleForm, BookingForm

# Create your views here.

class HomeView(View):
    def get(self, request):
        return render(request, 'home.html')
    
class BookView(View):
    def get(self, request):
        form = BookingForm()
        times_morning = ["8:00", "9:00", "10:00", "11:00"]
        times_afternoon = ["14:00", "15:00", "16:00", "17:00"]
        # ดึง slot ที่ถูกจองแล้วทั้งหมด
        booked_slots = list(Appointment.objects.values_list('date', 'time'))
        # แปลงเป็น string เพื่อใช้ใน JS
        booked_slots_str = [
            f"{date.strftime('%Y-%m-%d')}_{time.strftime('%-H:%M')}" for date, time in booked_slots
        ]
        return render(request, 'book.html', {
            'form': form,
            'times_morning': times_morning,
            'times_afternoon': times_afternoon,
            'booked_slots': booked_slots_str if booked_slots_str else [],
        })

    def post(self, request):
        form = BookingForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user_id = 1
            appointment.save()
            form.instance = appointment  # สำคัญ! ให้ฟอร์มรู้ว่า instance ที่ save คือ appointment นี้
            form.save_m2m()              # บันทึก ManyToMany ลง client_appointment_service_types
            return redirect('appointment')
        times_morning = ["8:00", "9:00", "10:00", "11:00"]
        times_afternoon = ["14:00", "15:00", "16:00", "17:00"]
        # ดึง slot ที่ถูกจองแล้วทั้งหมด
        booked_slots = list(Appointment.objects.values_list('date', 'time'))
        # แปลงเป็น string เพื่อใช้ใน JS
        booked_slots_str = [
            f"{date.strftime('%Y-%m-%d')}_{time.strftime('%-H:%M')}" for date, time in booked_slots
        ]
        return render(request, 'book.html', {
            'form': form,
            'times_morning': times_morning,
            'times_afternoon': times_afternoon,
            'booked_slots': booked_slots_str if booked_slots_str else [],
        })

class AppointmentView(View):
    def get(self, request):
        query = Appointment.objects.all().order_by('-id')
        appointments = []
        for ap in query:
            service = " , ".join(ap.service_types.values_list('name', flat=True))
            rating = Rating.objects.filter(appointment=ap).first()
            rating = rating.score if rating else None

            appointments.append({
                "id": ap.id,
                "license_plate": ap.car.license_plate if ap.car_id else None,
                "service": service,
                "date_time": ap.display_date_time(),
                "status": ap.status,
                "rating": rating
            })
        print(appointments)
        return render(request, 'appointment.html', {'appointments' : appointments})
    
class ReviewView(View):
    def get(self, request, appointment_id):
        return render(request, 'review.html')

class VehicleView(View):
    def get(self, request):
        query = Car.objects.all().order_by('id')
        vehicles = []
        for car in query:
            vehicles.append({
            'id' : car.id,
            'license_plate' : car.license_plate,
            'brand' : car.brand,
            'model' : car.model
            })
        print(vehicles)
        return render(request, 'vehicle.html', {'vehicles' : vehicles})

class AddVehicleView(View):
    def get(self, request):
        form = VehicleForm()
        return render(request, 'add_vehicle.html', {'form' : form})
    
    def post(self, request):
        form = VehicleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vehicle')
        return render(request, 'add_vehicle.html', {'form' : form})

class EditVehicleView(View):
    def get(self, request, car_id):
        vehicle = Car.objects.get(pk=car_id)
        form = VehicleForm(instance=vehicle)
        return render(request, 'edit_vehicle.html', {'form': form, 'car_id': car_id})

    def post(self, request, car_id):
        vehicle = Car.objects.get(pk=car_id)
        form = VehicleForm(request.POST, instance=vehicle)
        if form.is_valid():
            form.save()
            return redirect('vehicle')
        return render(request, 'edit_vehicle.html', {'form': form, 'car_id': car_id})
    
class DeleteVehicleView(View):
    def post(self, request, car_id):
        vehicle = Car.objects.get(pk=car_id)
        vehicle.delete()
        return redirect('vehicle')

class ProfileView(View):
    def get(self, request):
        return render(request, 'profile.html')

class EditProfileView(View):
    def get(self, request, user_id):
        return render(request, 'edit_profile.html')
    
