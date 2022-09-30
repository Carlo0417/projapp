# Generated by Django 3.2.15 on 2022-09-30 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dormitory', '0020_auto_20220930_1520'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='guardian_contact_no',
            field=models.CharField(default='none', max_length=20, verbose_name='number'),
        ),
        migrations.AddField(
            model_name='person',
            name='guardian_email_address',
            field=models.CharField(default='none', max_length=250, verbose_name='email'),
        ),
        migrations.AddField(
            model_name='person',
            name='guardian_first_name',
            field=models.CharField(default='none', max_length=250, verbose_name='first name'),
        ),
        migrations.AddField(
            model_name='person',
            name='guardian_last_name',
            field=models.CharField(default='none', max_length=250, verbose_name='last name'),
        ),
        migrations.AddField(
            model_name='person',
            name='guardian_present_address',
            field=models.CharField(default='none', max_length=250, verbose_name='address'),
        ),
    ]
