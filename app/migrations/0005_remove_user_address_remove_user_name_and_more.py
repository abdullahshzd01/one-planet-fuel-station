# Generated by Django 4.1.5 on 2023-01-30 10:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_remove_jobs_qualifications_jobs_job_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='address',
        ),
        migrations.RemoveField(
            model_name='user',
            name='name',
        ),
        migrations.RemoveField(
            model_name='user',
            name='password',
        ),
        migrations.RemoveField(
            model_name='user',
            name='usrName',
        ),
        migrations.AddField(
            model_name='jobs',
            name='fuelStation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.fuelstations'),
        ),
    ]