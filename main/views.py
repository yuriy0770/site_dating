from .models import Post
from django.shortcuts import redirect
from django.contrib import messages
from users.models import CustomUser
from django.shortcuts import get_object_or_404, render
from .models import Profile
from .models import Like
from django.contrib.auth.decorators import login_required
from .models import ChatRoom, Message
from django.db.models import Q
from django.shortcuts import render
from users.models import CustomUser
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import ChatRoom, Message


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
    """Список всех пользователей с поиском"""
    users = CustomUser.objects.all()
    query = request.GET.get('q')

    if query:
        users = users.filter(
            Q(username__icontains=query) |
            Q(city__icontains=query) |
            Q(profile__interests__icontains=query)
        ).distinct()

    return render(request, 'main/user_list.html', {'users': users, 'query': query})


def user_list_men(request):
    """Список мужчин"""
    users = CustomUser.objects.filter(profile__gender='M')
    return render(request, 'main/user_list.html', {'users': users, 'title': 'Мужчины'})


def user_list_women(request):
    """Список женщин"""
    users = CustomUser.objects.filter(profile__gender='F')
    return render(request, 'main/user_list.html', {'users': users, 'title': 'Женщины'})

def user_detail_by_id(request, user_id):
    """Просмотр анкеты по ID пользователя"""
    from users.models import CustomUser
    user = get_object_or_404(CustomUser, id=user_id)
    profile = user.profile
    profile.views_count += 1
    profile.save()
    return render(request, 'main/user_detail.html', {'profile': profile})


def user_detail(request, slug):
    profile = get_object_or_404(Profile, slug=slug)
    profile.views_count += 1
    profile.save()

    context = {
        'profile': profile,
    }

    if request.user.is_authenticated:
        user = request.user
        has_liked = Like.objects.filter(user=user, profile=profile).exists()
        has_mutual = Like.objects.filter(user=profile.user, profile=user.profile).exists()

        context['has_liked'] = has_liked
        context['has_mutual'] = has_mutual

    return render(request, 'main/user_detail.html', context)


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





@login_required
def like_user(request, user_id):
    to_user = get_object_or_404(CustomUser, id=user_id)
    from_user = request.user

    if from_user == to_user:
        messages.error(request, 'Нельзя лайкнуть себя')
        return redirect('main:user_detail', slug=to_user.profile.slug)

    profile = to_user.profile
    existing_like = Like.objects.filter(user=from_user, profile=profile).first()

    if existing_like:
        messages.warning(request, f'Вы уже лайкнули {to_user.username}')
    else:
        Like.objects.create(user=from_user, profile=profile)
        profile.likes_count += 1
        profile.save()
        messages.success(request, f'❤️ Вы лайкнули {to_user.username}')

        mutual_like = Like.objects.filter(user=to_user, profile=from_user.profile).exists()
        if mutual_like:
            existing_chat = ChatRoom.objects.filter(participants=from_user).filter(participants=to_user).first()
            if not existing_chat:
                chat = ChatRoom.objects.create()
                chat.participants.add(from_user, to_user)
                messages.success(request, f'🎉 Взаимный лайк! Чат с {to_user.username} открыт!')
            else:
                messages.info(request, f'У вас уже есть чат с {to_user.username}')

    return redirect('main:user_detail', slug=to_user.profile.slug)





@login_required
def chat_list(request):
    """Список чатов пользователя"""
    rooms = request.user.chat_rooms.filter(is_active=True)
    chat_data = []
    for room in rooms:
        other_user = room.participants.exclude(id=request.user.id).first()
        last_message = room.messages.last()
        chat_data.append({
            'room': room,
            'other_user': other_user,
            'last_message': last_message,
        })

    return render(request, 'main/chat_list.html', {'chat_data': chat_data})


@login_required
def chat_detail(request, room_id):
    """Страница чата"""
    room = get_object_or_404(ChatRoom, id=room_id, participants=request.user)
    messages_list = room.messages.all()
    other_user = room.participants.exclude(id=request.user.id).first()
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(room=room, author=request.user, content=content)
            return redirect('main:chat_detail', room_id=room.id)

    return render(request, 'main/chat_detail.html', {
        'room': room,
        'messages': messages_list,
        'other_user': other_user,
    })