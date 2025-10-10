import json

from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import redirect, render
from django.views import View

from core.models import Appointment, Vehicle, Review

from staff.forms import AppointmentStatusForm

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
        appointments =  Appointment.objects.all().order_by('-date', '-time')

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
        appointment = Appointment.objects.get(pk=appointment_id)
        form = AppointmentStatusForm(instance=appointment)
        status_choices = Appointment.Status.choices
        selected_status = form['status'].value() or appointment.status
        return render(request, 'appointment_edit.html', {
            'form': form,
            'appointment': appointment,
            'status_choices': status_choices,
            'selected_status': selected_status,
        })

    def post(self, request, appointment_id):
        appointment = Appointment.objects.get(pk=appointment_id)
        form = AppointmentStatusForm(request.POST, instance=appointment)
        status_choices = Appointment.Status.choices
        if form.is_valid():
            form.save()
            messages.success(request, f"Appointment (license plate: {appointment.vehicle.license_plate}) status updated successfully.")
            return redirect('appointment_list')

        selected_status = form['status'].value() or appointment.status
        return render(request, 'appointment_edit.html', {
            'form': form,
            'appointment': appointment,
            'status_choices': status_choices,
            'selected_status': selected_status,
        })

class VehicleListView(View):
    def get(self, request):
        vehicles = (
            Vehicle.objects
            .select_related('user')
            .order_by('id')
        )
        vehicle_rows = [
            {
                'index': idx,
                'id': vehicle.id,
                'username': vehicle.user.username if vehicle.user else '-',
                'license_plate': vehicle.license_plate,
                'brand': vehicle.brand,
                'model': vehicle.model,
            }
            for idx, vehicle in enumerate(vehicles, start=1)
        ]

        return render(request, 'vehicle_list.html', {
            'total_vehicles': vehicles.count(),
            'vehicles': vehicle_rows,
        })

class ReviewListView(View):
    def get(self, request):
        reviews = (
            Review.objects
            .select_related('appointment__vehicle', 'appointment__user')
            .order_by('id')
        )
        review_rows = []
        for idx, review in enumerate(reviews, start=1):
            appointment = review.appointment
            vehicle = appointment.vehicle if appointment else None
            review_rows.append({
                'index': idx,
                'id': review.id,
                'score': review.score,
                'comment': review.comment or '-',
                'appointment_number': appointment.id if appointment else '-',
                'license_plate': vehicle.license_plate if vehicle else '-',
            })
        return render(request, 'review_list.html', {
            'total_reviews': reviews.count(),
            'reviews': review_rows,
        })

class ReviewDetailView(View):
    def get(self, request, review_id):
        # Logic to retrieve and display details of a specific review
        return render(request, 'review_detail.html')
