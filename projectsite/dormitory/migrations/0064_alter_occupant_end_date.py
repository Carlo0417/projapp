# Generated by Django 3.2.15 on 2022-11-18 04:02

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('dormitory', '0063_auto_20221118_1200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='occupant',
            name='end_date',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
    ]
