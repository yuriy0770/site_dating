from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from users.forms import UserForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from main.models import Profile


@login_required
def complete_profile(request):
    """Заполнение профиля после регистрации"""
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user = request.user
        user.age = request.POST.get('age') or None
        user.city = request.POST.get('city')
        user.bio = request.POST.get('bio')
        if request.FILES.get('avatar'):
            user.avatar = request.FILES['avatar']
        user.save()

        profile.gender = request.POST.get('gender')
        profile.looking_for = request.POST.get('looking_for')
        profile.interests = request.POST.get('interests')
        profile.save()

        messages.success(request, 'Анкета успешно заполнена!')
        return redirect('main:index')

    return render(request, 'users/complete_profile.html', {'profile': profile})

def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('users:complete_profile')
    else:
        form = UserForm()
    return render(request, 'users/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request.POST, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('main:index')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('main:index')