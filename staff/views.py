import json

from django.db.models import Count
from django.shortcuts import render
from django.views import View

from django.contrib.auth.models import User

from core.models import Appointment, Vehicle, Review

# Create your views here.
class DashboardView(View):
    def get(self, request):
        total_appointments = Appointment.objects.count()
        total_vehicles = Vehicle.objects.count()
        total_users = User.objects.count()
        # Appointments over time for chart
        appointment_dates = list(
            Appointment.objects.values_list('date', flat=True)
        )
        appointment_dates_json = json.dumps(
            [date.isoformat() for date in appointment_dates]
        )
        # Rating statistics
        total_reviews = Review.objects.count()

        score_counts = dict(
            Review.objects.values('score')
            .annotate(total=Count('score'))
            .values_list('score', 'total')
        )

        rating_stats = []
        for score in range(1, 6):
            count = score_counts.get(score, 0)
            percentage = (count / total_reviews * 100) if total_reviews else 0
            rating_stats.append({
                'score': score,
                'count': count,
                'percentage': round(percentage, 2),
            })

        return render(request, 'dashboard.html', {
            'total_appointments': total_appointments,
            'total_vehicles': total_vehicles,
            'total_users': total_users,
            'appointment_dates_json': appointment_dates_json,
            'rating_stats': rating_stats,
            'total_reviews': total_reviews,
        })

class AppointmentListView(View):
    def get(self, request):
        appointments =  Appointment.objects.all().order_by('id')

        appointment_rows = []
        for idx, appointment in enumerate(appointments, start=1):
            service_list = ', '.join(appointment.service_types.values_list('name', flat=True))
            status_raw = appointment.status.upper()
            appointment_rows.append({
                'index': idx,
                'id': appointment.id,
                'license_plate': appointment.vehicle.license_plate if appointment.vehicle else '-',
                'services': service_list,
                'date': appointment.date.strftime('%d/%m/%Y'),
                'time': appointment.time.strftime('%H:%M'),
                'status': status_raw,
            })

        return render(request, 'appointment_list.html', {
            'total_appointments': appointments.count(),
            'appointments': appointment_rows,
        })

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
