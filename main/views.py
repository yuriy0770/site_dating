from django.shortcuts import render
from .models import Post, Profile

def index(request):
    profiles = Profile.objects.select_related('user').all()[:8]
    posts = Post.objects.select_related('author').prefetch_related('likes', 'comments').filter(is_published=True)[:6]
    context = {
        'profiles': profiles,
        'posts': posts,
    }
    return render(request, 'main/index.html', context)