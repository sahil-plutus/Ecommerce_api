# Generated by Django 4.0.2 on 2022-03-02 07:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('carts', '0003_orders_ordereditems'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orders',
            name='amount',
        ),
        migrations.RemoveField(
            model_name='orders',
            name='is_paid',
        ),
        migrations.RemoveField(
            model_name='orders',
            name='order_id',
        ),
        migrations.RemoveField(
            model_name='orders',
            name='payment_id',
        ),
        migrations.RemoveField(
            model_name='orders',
            name='payment_signature',
        ),
        migrations.AddField(
            model_name='orders',
            name='payment_method',
            field=models.CharField(choices=[('cash on delevery', 'cash on delevery'), ('online payment', 'online payment')], default='', max_length=22),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orders',
            name='shipping_charges',
            field=models.IntegerField(default=70),
        ),
        migrations.AlterField(
            model_name='cartitems',
            name='user',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]