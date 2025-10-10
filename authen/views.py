from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View

# Import authentication related modules
from django.contrib.auth import login, logout
from .forms import ProfileForm, SignUpForm, LoginForm
from django.contrib.auth.models import Group

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
        signup_form = SignUpForm()
        profile_form = ProfileForm()
        return render(request, 'signup.html', {
            "signup_form": signup_form, 
            "profile_form": profile_form
        })

    def post(self, request):
        signup_form = SignUpForm(request.POST)
        profile_form = ProfileForm(request.POST)

        if signup_form.is_valid() and profile_form.is_valid():
            # สร้าง user
            user = signup_form.save()
            # สร้าง profile พร้อมผูก user
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.pk = user.pk
            profile.save()
            # เพิ่ม user เข้า group client
            try:
                client_group = Group.objects.get(name='Client')
                user.groups.add(client_group)
            except Group.DoesNotExist:
                messages.warning(request, "Client group not found. Please contact administrator.")

            messages.success(request, "Account created successfully. Please log in.")
            return redirect('login')

        return render(request, 'signup.html', {
            "signup_form": signup_form, 
            "profile_form": profile_form
        })
