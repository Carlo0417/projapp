# Generated by Django 3.2.15 on 2023-04-22 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dormitory', '0091_auto_20230413_0139'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill_details',
            name='let_ref',
            field=models.CharField(default='None', max_length=250),
        ),
        migrations.AlterField(
            model_name='service',
            name='service_name',
            field=models.CharField(max_length=300),
        ),
    ]