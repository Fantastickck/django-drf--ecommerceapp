from wsgiref.simple_server import demo_app
from django.db import models
from django.contrib.auth.models import AbstractUser

from catalog.models import Product


class AdvUser(AbstractUser):
    email = models.EmailField(
        max_length=255, verbose_name='Электронная почта', unique=True)
    username = models.CharField(verbose_name='Имя пользователя', max_length=255, unique=True)
    password = models.CharField(max_length=255, verbose_name='Пароль')
    email_verify = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Profile(models.Model):
    user = models.OneToOneField(AdvUser, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=255, blank=True, verbose_name='Имя')
    last_name = models.CharField(max_length=255, blank=True, verbose_name='Фамилия')
    phone = models.CharField(max_length=255, blank=True, verbose_name='Номер телефона')
    date_of_birth = models.DateField(blank=True)
    default_address = models.CharField(max_length=255, blank=True, verbose_name='Адрес')
    slug = models.SlugField(max_length=255, unique=True, blank=True, verbose_name='URL пользователя')

    def __str__(self):
        return self.slug

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class Feedback(models.Model):
    text = models.TextField(verbose_name='Текст отзыва')
    rating = models.IntegerField(verbose_name='Оценка')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name='Продукт')
    user = models.ForeignKey(AdvUser, on_delete=models.PROTECT, verbose_name='Пользователь')

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
