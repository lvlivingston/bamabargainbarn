# Generated by Django 5.0 on 2023-12-20 15:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_alter_customer_state_alter_customer_street_address'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='streetAddress',
            new_name='street_address',
        ),
    ]