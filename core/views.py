from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from accounts.forms import UserLoginForm, UserRegistrationForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect('core:dashboard')
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.get_full_name() or user.email}!')
                next_url = request.POST.get('next') or request.GET.get('next') or '/'
                return redirect(next_url)
            else:
                form.add_error('email', 'Invalid email or password.')
    else:
        form = UserLoginForm()
    return render(request, 'registration/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('accounts:login')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('core:dashboard')
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            role = form.cleaned_data['role']
            if role == 'student':
                from students.models import Student
                Student.objects.create(
                    user=user,
                    student_id=f'STU{user.id:04d}',
                )
            elif role == 'teacher':
                from teachers.models import Teacher
                Teacher.objects.create(
                    user=user,
                    employee_id=f'EMP{user.id:04d}',
                )
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('accounts:login')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def profile_view(request):
    return render(request, 'profile.html')
