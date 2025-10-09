from django.shortcuts import render
from django.views import View

# Create your views here.
class DashboardView(View):
    def get(self, request):
        return render(request, 'dashboard.html')

class AppointmentListView(View):
    def get(self, request):
        # Logic to retrieve and display a list of appointments
        return render(request, 'appointment_list.html')

class AppointmentDetailView(View):
    def get(self, request, appointment_id):
        # Logic to retrieve and display details of a specific appointment
        return render(request, 'appointment_detail.html')

class AppointmentEditView(View):
    def get(self, request, appointment_id):
        # Logic to edit the status of a specific appointment
        return render(request, 'appointment_edit.html')

class VehicleListView(View):
    def get(self, request):
        # Logic to retrieve and display a list of vehicles
        return render(request, 'vehicle_list.html')

class ReviewListView(View):
    def get(self, request):
        # Logic to retrieve and display a list of reviews
        return render(request, 'review_list.html')

class ReviewDetailView(View):
    def get(self, request, review_id):
        # Logic to retrieve and display details of a specific review
        return render(request, 'review_detail.html')
