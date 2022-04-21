# Generated by Django 3.1 on 2022-04-21 11:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0021_productimage'),
        ('user_product', '0004_favourites'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='favourites',
            name='product',
        ),
        migrations.CreateModel(
            name='FavouritesItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('favourites', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='user_product.favourites', verbose_name='Избранный товар')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favourites_items', to='catalog.product', verbose_name='Товар')),
            ],
        ),
    ]
