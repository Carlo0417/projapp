# Generated by Django 3.2.15 on 2022-10-02 12:48

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('dormitory', '0021_auto_20220930_1522'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='bill_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='bill',
            name='due_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
