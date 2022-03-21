# Generated by Django 4.0.2 on 2022-03-14 12:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_delete_csvfile'),
        ('carts', '0018_remove_invoice_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordereditems',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='product.product'),
        ),
        migrations.CreateModel(
            name='InvoiceItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='carts.invoice')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoice_product', to='product.product')),
            ],
        ),
    ]
