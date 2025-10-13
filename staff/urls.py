from django.urls import path
from . import views

urlpatterns = [
    # ex: /staff/
    path('', views.DashboardView.as_view(), name='dashboard'),
    # ex: /staff/appointments/
    path('appointments/', views.AppointmentListView.as_view(), name='appointment_list'),
    # ex: /staff/appointments/1/
    path('appointments/<int:appointment_id>/', views.AppointmentDetailView.as_view(), name='appointment_detail'),
    # ex: /staff/appointments/1/edit/
    path('appointments/<int:appointment_id>/edit/', views.AppointmentEditView.as_view(), name='appointment_edit'),
    # ex: /staff/vehicles/
    path('vehicles/', views.VehicleListView.as_view(), name='vehicle_list'),
    # ex: /staff/vehicles/1/delete/
    path('vehicles/<int:vehicle_id>/delete/', views.VehicleDeleteView.as_view(), name='delete_vehicle_list'),
    # ex: /staff/reviews/
    path('reviews/', views.ReviewListView.as_view(), name='review_list'),
    # ex: /staff/reviews/1/
    path('reviews/<int:review_id>/', views.ReviewDetailView.as_view(), name='review_detail'),
    # ex: /staff/users/
    path('users/', views.UserListView.as_view(), name='user_list'),
    # ex: /staff/users/1/detail/
    path('users/<int:user_id>/detail/', views.UserDetailView.as_view(), name='detail_user_list'),
    # ex: /staff/users/1/delete/
    path('users/<int:user_id>/delete/', views.UserDeleteView.as_view(), name='delete_user_list'),
]
