# Generated by Django 4.1.5 on 2023-05-07 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_remove_applicant_job_applicant_job'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='productList',
            field=models.ManyToManyField(to='app.products'),
        ),
    ]