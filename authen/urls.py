from django.urls import path

from authen.views import LoginView, LogoutView, SignupView, UnauthorizedView
from client.views import HomeView


urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('signup/', SignupView.as_view(), name="signup"),
    path('unauthorized/', UnauthorizedView.as_view(), name="unauthorized"),
]