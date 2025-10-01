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

class VehicleView(View):
    def get(self, request):
        return render(request, 'vehicle.html')