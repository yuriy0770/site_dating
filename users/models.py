from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15, unique=True, verbose_name='Телефон')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name='Аватар')
    bio = models.TextField(max_length=500, null=True, blank=True, verbose_name='О себе')
    age = models.IntegerField(null=True, blank=True, verbose_name='Возраст')
    city = models.CharField(max_length=100, null=True, blank=True, verbose_name='Город')
    is_verified = models.BooleanField(default=False, verbose_name='Верифицирован')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'