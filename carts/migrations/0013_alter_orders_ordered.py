# Generated by Django 4.0.2 on 2022-03-11 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0012_alter_orders_ordered'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='ordered',
            field=models.BooleanField(choices=[(True, 'Successfull'), (False, 'Pending')], default=False),
        ),
    ]
