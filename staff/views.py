import json

from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import redirect, render
from django.views import View

from core.models import Appointment, Vehicle, Review

from staff.forms import AppointmentStatusForm

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

# Create your views here.
class DashboardView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ['staff.access_dashboard']

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

class AppointmentListView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ['staff.access_appointment_page']

    def get(self, request):
        appointments =  Appointment.objects.all().order_by('-date', '-time')
        filter_date = request.GET.get('date')
        filter_status = request.GET.get('status')

        if filter_date:
            appointments = appointments.filter(date=filter_date)
        if filter_status:
            appointments = appointments.filter(status__iexact=filter_status)

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
            'filter_date': filter_date,
            'filter_status': filter_status,
        })

class AppointmentDetailView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ['staff.access_appointment_page', 'staff.view_appointmentstaff']

    def get(self, request, appointment_id):
        appointment_detail = Appointment.objects.get(pk=appointment_id)
        vehicle = appointment_detail.vehicle if appointment_detail.vehicle_id else None
        license_plate = vehicle.license_plate
        brand = vehicle.brand if vehicle else '-'
        model = vehicle.model if vehicle else '-'
        services = ', '.join(appointment_detail.service_types.values_list('name', flat=True))

        return render(request, 'appointment_detail.html', {
            'appointment': appointment_detail,
            'license_plate': license_plate,
            'brand': brand,
            'model': model,
            'services': services,
            'formatted_date': appointment_detail.date.strftime('%d / %m / %Y'),
            'formatted_time': appointment_detail.time.strftime('%H:%M'),
            'description': appointment_detail.description or '-',
        })

class AppointmentEditView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ['staff.access_appointment_page', 'staff.change_appointmentstaff']

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

class VehicleListView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ['staff.access_vehicle_page']
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

class ReviewListView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ['staff.access_review_page', 'staff.view_review']

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

class ReviewDetailView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ['staff.access_review_page', 'staff.view_review']
    def get(self, request, review_id):
        review = Review.objects.get(pk=review_id)
        appointment = review.appointment
        vehicle = appointment.vehicle if appointment else None
        services = list(appointment.service_types.values_list('name', flat=True)) if appointment else []
        if not services:
            services = ['-']

        review_data = {
            'review': review,
            'license_plate': vehicle.license_plate,
            'brand': vehicle.brand,
            'model': vehicle.model,
            'formatted_date': appointment.date.strftime('%d / %m / %Y') if appointment else '-',
            'formatted_time': appointment.time.strftime('%H:%M'),
            'services': services,
            'description': appointment.description or '-' if appointment else '-',
            'score': review.score,
            'comment': review.comment or '-',
        }
        return render(request, 'review_detail.html', review_data)
