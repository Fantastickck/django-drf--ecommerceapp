# Generated by Django 3.1 on 2022-04-20 18:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0019_product_quantity_of_orders'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='quantity_of_orders',
            new_name='quantity_of_purchases',
        ),
    ]
