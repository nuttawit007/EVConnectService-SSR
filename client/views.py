from django.shortcuts import render
from django.views import View
from client.models import *

# Create your views here.

class HomeView(View):
    def get(self, request):
        return render(request, 'home.html')
    
class BookView(View):
    def get(self, request):
        return render(request, 'book.html')

class AppointmentView(View):
    def get(self, request):
        query = Appointment.objects.all().order_by('date', 'time')
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
        return render(request, 'vehicle.html')

class AddVehicleView(View):
    def get(self, request):
        return render(request, 'add_vehicle.html')

class EditVehicleView(View):
    def get(self, request, car_id):
        return render(request, 'edit_vehicle.html')

class ProfileView(View):
    def get(self, request):
        return render(request, 'profile.html')

class EditProfileView(View):
    def get(self, request, user_id):
        return render(request, 'edit_profile.html')
    
