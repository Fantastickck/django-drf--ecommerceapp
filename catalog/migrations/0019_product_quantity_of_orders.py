# Generated by Django 3.1 on 2022-04-20 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0018_auto_20220420_2140'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='quantity_of_orders',
            field=models.PositiveIntegerField(default=0, verbose_name='Количество заказов товара'),
        ),
    ]
