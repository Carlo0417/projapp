# Generated by Django 3.2.15 on 2022-10-13 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dormitory', '0034_auto_20221012_2138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bed',
            name='bed_code',
            field=models.CharField(default='none', max_length=25, verbose_name='Bed Code'),
        ),
    ]