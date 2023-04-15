# Generated by Django 4.1.5 on 2023-03-04 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_products_fuelstation_alter_products_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='fuelstations',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True, verbose_name='last login'),
        ),
        migrations.AlterField(
            model_name='fuelstations',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
