from django.db import models

from main.models import AdvUser

class Room(models.Model):
    user = models.ManyToManyField(AdvUser, verbose_name='Участник', blank=True)

    def __str__(self):
        return '{}'.format(self.id)

    class Meta:
        verbose_name = 'Комната'
        verbose_name_plural = 'Комнаты'
    

class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='messages', verbose_name='Сообщение')
    author = models.ForeignKey(AdvUser, on_delete=models.CASCADE, related_name='authors', verbose_name='Автор сообщения')
    text = models.TextField(verbose_name='Текст сообщения')
    created_at = models.DateTimeField(auto_now=True, verbose_name='Дата создания сообщения')

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['created_at']


