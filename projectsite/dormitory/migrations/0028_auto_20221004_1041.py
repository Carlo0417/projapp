# Generated by Django 3.2.15 on 2022-10-04 10:41

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('dormitory', '0027_person_boarder_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bill_details',
            name='bill',
        ),
        migrations.AddField(
            model_name='bill_details',
            name='bill_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='bill_details',
            name='occupant',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='dormitory.occupant'),
        ),
    ]