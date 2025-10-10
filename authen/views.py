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

            next_url = request.GET.get('next') or request.POST.get('next')
            if next_url:
                return redirect(next_url)
        
            # เช็ค group แล้วค่อยส่งไปหน้าเฉพาะ
            if request.user.is_superuser or request.user.groups.filter(name="Staff").exists():
                return redirect('dashboard')   # เปลี่ยนเป็นชื่อ url name ของคุณ
            elif request.user.groups.filter(name="Client").exists():
                return redirect('home')  # ถ้ามี dashboard ของลูกค้า
            else:
                return redirect('home')

        messages.error(request, "username or password is incorrect")
        return render(request,'login.html', {"form":form})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')

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
