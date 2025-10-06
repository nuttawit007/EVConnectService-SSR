from django.urls import path
from . import views

urlpatterns = [
    # ex: /client/
    path('', views.HomeView.as_view(), name='home'),
    # ex: /client/book/
    path('book/', views.BookView.as_view(), name='book'),
    # ex: /client/appointment/
    path('appointment/', views.AppointmentView.as_view(), name='appointment'),
    # ex: /client/appointment/1/review
    path('appointment/<int:appointment_id>/review/', views.ReviewView.as_view(), name='review'),
    # ex: /client/vehicle/
    path('vehicle/', views.VehicleView.as_view(), name='vehicle'),
    # ex: /client/vehicle/add/
    path('vehicle/add', views.AddVehicleView.as_view(), name='add_vehicle'),
    # ex: /client/vehicle/1/edit
    path('vehicle/<int:car_id>/edit/', views.EditVehicleView.as_view(), name='edit_vehicle'),
    # ex: /client/vehicle/1/delete
    path('vehicle/<int:car_id>/delete/', views.DeleteVehicleView.as_view(), name='delete_vehicle'),
    # ex: /client/profile/
    path('profile/', views.ProfileView.as_view(), name='profile'),
    # ex: /client/profile/1/edit
    path('profile/<int:user_id>/edit/', views.EditProfileView.as_view(), name='edit_profile'),
]