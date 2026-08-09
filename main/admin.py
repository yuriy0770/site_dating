from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Profile, Post, Comment, Like
from users.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'phone', 'is_verified', 'is_staff', 'created_at')
    list_filter = ('is_verified', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'phone')
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительно', {'fields': ('phone', 'avatar', 'bio', 'age', 'city', 'is_verified', 'created_at')}),
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender', 'looking_for', 'views_count', 'likes_count', 'last_active')
    list_filter = ('gender', 'looking_for')
    search_fields = ('user__username', 'user__email')
    # Убираем prepopulated_fields или делаем через метод
    readonly_fields = ('views_count', 'likes_count')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'content_preview', 'created_at', 'is_published')
    list_filter = ('is_published', 'created_at')
    search_fields = ('author__username', 'content')
    # Убираем prepopulated_fields
    readonly_fields = ('created_at', 'updated_at', 'slug')  # Добавил slug для наглядности

    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Контент (превью)'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'content_preview', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('author__username', 'content')

    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Комментарий (превью)'


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'profile', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username',)