# Generated by Django 4.0.2 on 2022-03-14 10:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0017_invoice'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='product',
        ),
    ]
