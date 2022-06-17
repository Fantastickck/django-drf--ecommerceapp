from django.db import models
from django.contrib.auth.models import AbstractUser


class AdvUser(AbstractUser):
    """
    Модель пользователя
    """
    email = models.EmailField(
        max_length=255, verbose_name='Электронная почта', unique=True)
    username = models.CharField(
        verbose_name='Имя пользователя', max_length=255, unique=True)
    password = models.CharField(max_length=255, verbose_name='Пароль')
    email_verify = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Profile(models.Model):
    """
    Модель профиля пользователя
    """
    user = models.OneToOneField(
        AdvUser, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(
        max_length=255, blank=True, verbose_name='Имя')
    last_name = models.CharField(
        max_length=255, blank=True, verbose_name='Фамилия')
    image = models.ImageField(
        blank=True, upload_to='profile_images', verbose_name='Изображение профиля')
    phone = models.CharField(max_length=255, blank=True,
                             verbose_name='Номер телефона')
    date_of_birth = models.DateField(blank=True)
    default_address = models.CharField(
        max_length=255, blank=True, verbose_name='Адрес')
    slug = models.SlugField(max_length=255, unique=True,
                            blank=True, verbose_name='URL пользователя')

    def __str__(self):
        return self.slug

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
