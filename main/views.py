from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile, Post
from users.models import CustomUser


def index(request):
    """Главная страница"""
    profiles = Profile.objects.select_related('user').all()[:8]
    posts = Post.objects.select_related('author').filter(is_published=True)[:6]
    context = {
        'profiles': profiles,
        'posts': posts,
    }
    return render(request, 'main/index.html', context)


def user_list(request):
    """Список всех пользователей (анкет)"""
    users = CustomUser.objects.all()
    return render(request, 'main/user_list.html', {'users': users})


def user_list_men(request):
    """Список мужчин"""
    users = CustomUser.objects.filter(profile__gender='M')
    return render(request, 'main/user_list.html', {'users': users, 'title': 'Мужчины'})


def user_list_women(request):
    """Список женщин"""
    users = CustomUser.objects.filter(profile__gender='F')
    return render(request, 'main/user_list.html', {'users': users, 'title': 'Женщины'})


def user_detail(request, slug):
    """Просмотр анкеты другого пользователя"""
    profile = get_object_or_404(Profile, slug=slug)
    profile.views_count += 1
    profile.save()
    return render(request, 'main/user_detail.html', {'profile': profile})


@login_required
def profile_view(request):
    """Личный кабинет пользователя (своя анкета)"""
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, 'main/profile.html', {'profile': profile})


@login_required
def profile_edit(request):
    """Редактирование своей анкеты"""
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user = request.user
        user.username = request.POST.get('username', user.username)
        user.age = request.POST.get('age', user.age)
        user.city = request.POST.get('city', user.city)
        user.bio = request.POST.get('bio', user.bio)
        if request.FILES.get('avatar'):
            user.avatar = request.FILES['avatar']
        user.save()

        profile.gender = request.POST.get('gender', profile.gender)
        profile.looking_for = request.POST.get('looking_for', profile.looking_for)
        profile.interests = request.POST.get('interests', profile.interests)
        profile.save()

        messages.success(request, 'Анкета успешно обновлена!')
        return redirect('main:profile_view')

    return render(request, 'main/profile_edit.html', {'profile': profile})