# Generated by Django 5.0 on 2023-12-13 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0010_product_rating_product_totalrating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='totalRating',
            field=models.IntegerField(),
        ),
    ]