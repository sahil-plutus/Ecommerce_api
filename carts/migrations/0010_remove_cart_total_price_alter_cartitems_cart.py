# Generated by Django 4.0.2 on 2022-03-10 12:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0009_alter_orders_total_amount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='total_price',
        ),
        migrations.AlterField(
            model_name='cartitems',
            name='cart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_items', to='carts.cart'),
        ),
    ]
