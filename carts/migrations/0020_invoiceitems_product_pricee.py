# Generated by Django 4.0.2 on 2022-03-15 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0019_alter_ordereditems_product_invoiceitems'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoiceitems',
            name='product_pricee',
            field=models.FloatField(default=0),
        ),
    ]
