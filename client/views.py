from django.shortcuts import render
from django.views import View

# Create your views here.

class HomeView(View):
    def get(self, request):
        return render(request, 'home.html')
    
class BookView(View):
    def get(self, request):
        return render(request, 'book.html')

class AppointmentView(View):
    def get(self, request):
        return render(request, 'appointment.html')
    
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
    
