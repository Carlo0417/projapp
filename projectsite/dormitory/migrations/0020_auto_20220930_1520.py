# Generated by Django 3.2.15 on 2022-09-30 07:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dormitory', '0019_auto_20220930_1517'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='guardian_contact_no',
        ),
        migrations.RemoveField(
            model_name='person',
            name='guardian_email_address',
        ),
        migrations.RemoveField(
            model_name='person',
            name='guardian_first_name',
        ),
        migrations.RemoveField(
            model_name='person',
            name='guardian_last_name',
        ),
        migrations.RemoveField(
            model_name='person',
            name='guardian_present_address',
        ),
    ]
