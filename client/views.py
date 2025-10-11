from django.shortcuts import render, redirect
from django.views import View

from core.models import Appointment, Review, Vehicle

from client.forms import VehicleForm, BookingForm, ReviewForm, UserForm, ProfileForm, PasswordChangeForm

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

# Create your views here.
class HomeView(View):
    def get(self, request):
        return render(request, 'home.html')

class BookView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ['client.access_booking_page']

    def get(self, request):
        form = BookingForm()
        form.fields['vehicle'].queryset = Vehicle.objects.filter(user=request.user)

        # เลือกรถคันแรกเป็น default ถ้ามี
        first_vehicle = form.fields['vehicle'].queryset.first()
        default_vehicle = str(first_vehicle.pk) if first_vehicle else None
        if first_vehicle:
            form.initial['vehicle'] = first_vehicle.pk

        # หา service ที่ชื่อ "Maintenance" จาก queryset ของฟิลด์ service_types
        services_qs = form.fields['service_types'].queryset
        maintenance = services_qs.filter(name__iexact='maintenance').first()
        default_services = []
        if maintenance:
            # ตั้งค่า default เป็นรายการ id (สำหรับ ModelMultipleChoiceField)
            form.initial['service_types'] = [maintenance.pk]
            default_services = [str(maintenance.pk)]  # ให้เป็น string เพื่อจะเช็คใน template ได้ง่าย

        times_morning = ["8:00", "9:00", "10:00", "11:00"]
        times_afternoon = ["14:00", "15:00", "16:00", "17:00"]
        # ดึง slot ที่ถูกจองแล้วทั้งหมด
        booked_slots = list(Appointment.objects.values_list('date', 'time'))
        # แปลงเป็น string เพื่อใช้ใน JS
        booked_slots_str = [
            f"{date.strftime('%Y-%m-%d')}_{time.strftime('%-H:%M')}" for date, time in booked_slots
        ]
        print("Default vehicle:", default_vehicle)
        print("Default services:", default_services)
        return render(request, 'book.html', {
            'form': form,
            'times_morning': times_morning,
            'times_afternoon': times_afternoon,
            'booked_slots': booked_slots_str if booked_slots_str else [],
            'default_services': default_services,
            'default_vehicle': default_vehicle,
        })

    def post(self, request):
        form = BookingForm(request.POST)
        form.fields['vehicle'].queryset = Vehicle.objects.filter(user=request.user)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user
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

class AppointmentView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ['client.access_appointment_page']

    def get(self, request):
        appointments = Appointment.objects.filter(user=request.user).order_by('-id')
        appointment_rows = []
        for ap in appointments:
            service = " , ".join(ap.service_types.values_list('name', flat=True)) 
            review = Review.objects.filter(appointment=ap).first()
            review_score = review.score if review else None

            appointment_rows.append({
                "id": ap.id,
                "license_plate": ap.vehicle.license_plate if ap.vehicle_id else None,
                "service": service,
                "date_time": ap.display_date_time(),
                "status": ap.status,
                "review_score": review_score,
            })
        print(appointment_rows)
        return render(request, 'appointment.html', {'appointments' : appointment_rows})

class ReviewView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ['client.access_review_page']

    def get(self, request, appointment_id):
        form = ReviewForm()
        appointment = Appointment.objects.get(pk=appointment_id)
        score = ['1', '2', '3', '4', '5']
        return render(request, 'review.html', {
            'form': form,
            'appointment': appointment, 
            'score': score
        })
    
    def post(self, request, appointment_id):
        form = ReviewForm(request.POST)
        score = ['1', '2', '3', '4', '5']
        appointment = Appointment.objects.get(pk=appointment_id)
        if form.is_valid():
            review = form.save(commit=False)
            review.appointment = appointment
            review.save()
            return redirect('appointment')
        return render(request, 'review.html', {
            'form': form,
            'appointment': appointment,
            'score': score
        })

class VehicleView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ['client.access_vehicle_page']

    def get(self, request):
        query = Vehicle.objects.filter(user=request.user).order_by('id')
        vehicles = []
        for vehicle in query:
            vehicles.append({
            'id' : vehicle.id,
            'license_plate' : vehicle.license_plate,
            'brand' : vehicle.brand,
            'model' : vehicle.model
            })
        print(vehicles)
        return render(request, 'vehicle.html', {'vehicles' : vehicles})

class AddVehicleView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ['client.access_vehicle_page']

    def get(self, request):
        form = VehicleForm()
        return render(request, 'add_vehicle.html', {'form' : form})
    
    def post(self, request):
        form = VehicleForm(request.POST)
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.user = request.user  # กำหนด user เป็นคนที่ login
            vehicle.save()
            return redirect('vehicle')
        return render(request, 'add_vehicle.html', {'form' : form})

class EditVehicleView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ['client.access_vehicle_page', 'client.change_vehicleclient']
    def get(self, request, vehicle_id):
        vehicle = Vehicle.objects.get(pk=vehicle_id)
        form = VehicleForm(instance=vehicle)
        return render(request, 'edit_vehicle.html', {'form': form, 'vehicle_id': vehicle_id})

    def post(self, request, vehicle_id):
        vehicle = Vehicle.objects.get(pk=vehicle_id)
        form = VehicleForm(request.POST, instance=vehicle)
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.user = request.user  # กำหนด user เป็นคนที่ login
            vehicle.save()
            return redirect('vehicle')
        return render(request, 'edit_vehicle.html', {'form': form, 'vehicle_id': vehicle_id})

class DeleteVehicleView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ['client.access_vehicle_page', 'client.delete_vehicleclient']

    def post(self, request, vehicle_id):
        vehicle = Vehicle.objects.get(pk=vehicle_id)
        print(vehicle)
        vehicle.delete()
        return redirect('vehicle')

class ProfileView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ['client.access_profile_page']
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')

        user = request.user
        profile = getattr(user, "profile", None)
        raw_phone = getattr(profile, "phone_number", None)
        phone_number_display = "-"
        if raw_phone:
            normalized = str(raw_phone).strip().lower()
            if normalized not in {"null", "[null]"}:
                phone_number_display = raw_phone

        return render(
            request,
            'profile.html',
            {
                'user': user,
                'profile': profile,
                'phone_number_display': phone_number_display,
            },
        )

class EditProfileView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ['client.access_profile_page', 'client.change_profileclient']

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')

        user = request.user
        profile = getattr(user, "profile", None)
        form_user = UserForm(instance=user)
        form_profile = ProfileForm(instance=profile)
        return render(request, 'edit_profile.html', {'form_user': form_user, 'form_profile': form_profile})

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('login')

        user = request.user
        profile = getattr(user, "profile", None)
        form_user = UserForm(request.POST, instance=user)
        form_profile = ProfileForm(request.POST, instance=profile)
        if form_user.is_valid() and form_profile.is_valid():
            form_user.save()
            form_profile.save()
            return redirect('profile')
        return render(request, 'edit_profile.html', {'form_user': form_user, 'form_profile': form_profile})

class PasswordChangeView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ['client.access_profile_page', 'client.change_profileclient']

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        form = PasswordChangeForm(user=request.user)
        return render(request, 'change_password.html', {'form': form})

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('login')

        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('profile')
        return render(request, 'change_password.html', {'form': form})