# Generated by Django 3.1 on 2022-04-19 16:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalog', '0015_auto_20220419_0851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='category',
            field=models.ManyToManyField(blank=True, related_name='brands', to='catalog.Category'),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedbacks', to='catalog.product', verbose_name='Продукт'),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='product',
            name='brand',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='catalog.brand', verbose_name='Бренд'),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='catalog.category', verbose_name='Категория'),
        ),
        migrations.CreateModel(
            name='Favourites',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favourites', to='catalog.product', verbose_name='Продукт')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='favourites', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Избранное',
                'verbose_name_plural': 'Избранное',
            },
        ),
    ]
