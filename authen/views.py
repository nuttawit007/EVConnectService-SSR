from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View

# Import authentication related modules
from django.contrib.auth import login, logout
from .forms import SignUpForm, LoginForm

class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {"form": form})

    def post(self, request):
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user() 
            login(request,user)
            return redirect('home')  

        messages.error(request, "username or password is incorrect")
        return render(request,'login.html', {"form":form})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')

class SignupView(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, 'signup.html', {"form": form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully. Please log in.")
            return redirect('login')

        return render(request, 'signup.html', {"form": form})
