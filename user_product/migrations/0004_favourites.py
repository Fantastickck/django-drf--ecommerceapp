# Generated by Django 3.1 on 2022-04-21 11:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalog', '0021_productimage'),
        ('user_product', '0003_auto_20220421_1631'),
    ]

    operations = [
        migrations.CreateModel(
            name='Favourites',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favourites', to='catalog.product', verbose_name='Товар')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='favourites', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Избранное',
                'verbose_name_plural': 'Избранное пользователей',
            },
        ),
    ]
