# Generated by Django 3.2.15 on 2023-01-02 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dormitory', '0080_user_person_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(default='', max_length=20, verbose_name='Contact Number'),
        ),
    ]
