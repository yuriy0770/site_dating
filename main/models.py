from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.utils import timezone

from users.models import CustomUser

User = get_user_model()


class Profile(models.Model):
    """Анкета пользователя (расширение)"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name='Пользователь')
    slug = models.SlugField(max_length=200, unique=True, blank=True, verbose_name='Слаг')
    gender = models.CharField(max_length=10, choices=[('M', 'Мужской'), ('F', 'Женский')], verbose_name='Пол')
    looking_for = models.CharField(max_length=10, choices=[('M', 'Мужской'), ('F', 'Женский'), ('A', 'Все')],
                                   default='A', verbose_name='Ищет')
    interests = models.TextField(blank=True, verbose_name='Интересы')
    height = models.IntegerField(null=True, blank=True, verbose_name='Рост')
    weight = models.IntegerField(null=True, blank=True, verbose_name='Вес')
    views_count = models.PositiveIntegerField(default=0, verbose_name='Просмотры')
    likes_count = models.PositiveIntegerField(default=0, verbose_name='Лайки')
    last_active = models.DateTimeField(auto_now=True, verbose_name='Последняя активность')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.user.username}-{self.user.id}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Анкета {self.user.username}"

    class Meta:
        verbose_name = 'Анкета'
        verbose_name_plural = 'Анкеты'


class Post(models.Model):
    """Пост в ленте новостей"""
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', verbose_name='Автор')
    content = models.TextField(max_length=2000, verbose_name='Контент')
    image = models.ImageField(upload_to='posts/', null=True, blank=True, verbose_name='Изображение')
    slug = models.SlugField(max_length=200, unique=True, blank=True, verbose_name='Слаг')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлен')
    is_published = models.BooleanField(default=True, verbose_name='Опубликован')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.author.username}-{self.id or timezone.now().timestamp()}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Пост {self.author.username}: {self.content[:50]}"

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-created_at']


class Comment(models.Model):
    """Комментарий к посту"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='Пост')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name='Автор')
    content = models.TextField(max_length=1000, verbose_name='Текст комментария')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')

    def __str__(self):
        return f"Комментарий {self.author.username} к {self.post}"

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-created_at']


class Like(models.Model):
    """Лайк (для постов и анкет)"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes', verbose_name='Кто лайкнул')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True, related_name='likes', verbose_name='Пост')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True, related_name='likes', verbose_name='Анкета')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')

    class Meta:
        unique_together = [['user', 'post'], ['user', 'profile']]
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'

    def __str__(self):
        if self.post:
            return f"{self.user} лайкнул пост {self.post.id}"
        return f"{self.user} лайкнул анкету {self.profile.user.username}"

class ChatRoom(models.Model):
    """Комната чата между двумя пользователями"""
    participants = models.ManyToManyField(CustomUser, related_name='chat_rooms', verbose_name='Участники')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    is_active = models.BooleanField(default=True, verbose_name='Активен')

    def __str__(self):
        return f"Чат {self.id}"

    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'


class Message(models.Model):
    """Сообщение в чате"""
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages', verbose_name='Комната')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='messages', verbose_name='Автор')
    content = models.TextField(max_length=2000, verbose_name='Текст')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    is_read = models.BooleanField(default=False, verbose_name='Прочитано')

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.author.username}: {self.content[:30]}"