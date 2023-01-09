# Generated by Django 3.2.15 on 2023-01-02 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dormitory', '0078_auto_20230102_1707'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='person_id',
        ),
        migrations.AddField(
            model_name='user',
            name='phone_number',
            field=models.IntegerField(blank=True, max_length=15, null=True),
        ),
    ]