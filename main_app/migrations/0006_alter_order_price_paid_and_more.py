# Generated by Django 5.0 on 2023-12-20 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_order_price_with_shipping'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='price_paid',
            field=models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='price_with_shipping',
            field=models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=10, null=True),
        ),
    ]