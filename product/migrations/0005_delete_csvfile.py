# Generated by Django 4.0.2 on 2022-03-10 12:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_csvfile'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CsvFile',
        ),
    ]
