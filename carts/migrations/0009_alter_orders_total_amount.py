# Generated by Django 4.0.2 on 2022-03-03 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0008_remove_orders_cart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='total_amount',
            field=models.FloatField(blank=True),
        ),
    ]
