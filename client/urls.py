from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('book/', views.BookView.as_view(), name='book'),
    path('appointment/', views.AppointmentView.as_view(), name='appointment'),
    path('vehicle/', views.VehicleView.as_view(), name='vehicle'),
]