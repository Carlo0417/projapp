# Generated by Django 3.2.15 on 2022-11-14 05:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dormitory', '0060_alter_bill_details_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bill_details',
            name='quantity',
        ),
    ]
