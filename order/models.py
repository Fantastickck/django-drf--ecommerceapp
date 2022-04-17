from turtle import ondrag
from django.db import models

from catalog.models import Product
from main.models import AdvUser


class Order(models.Model):
    user = models.ForeignKey(AdvUser, blank=True, null=True, verbose_name='Пользователь', on_delete=models.SET_NULL)
    first_name = models.CharField(max_length=255, verbose_name='Имя')
    last_name = models.CharField(max_length=255, verbose_name='Фамилия')
    email = models.EmailField(verbose_name='Эл. почта')
    phone = models.CharField(max_length=255, verbose_name='Номер телефона')
    address = models.CharField(max_length=255, verbose_name='Адрес')
    created_date = models.DateTimeField(auto_now=True, verbose_name='Дата создания заказа')
    paid = models.BooleanField(default=False, verbose_name='Оплачено')

    class Meta:
        ordering = ['-created_date',]
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, verbose_name='Заказ', related_name='items', on_delete=models.PROTECT)
    product = models.ForeignKey(Product, verbose_name='Товар', related_name='order_items', on_delete=models.PROTECT)
    price = models.PositiveIntegerField(verbose_name='Цена')
    quantity = models.PositiveIntegerField(verbose_name='Количество')

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity
