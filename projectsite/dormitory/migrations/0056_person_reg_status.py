# Generated by Django 3.2.15 on 2022-11-02 01:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dormitory', '0055_remove_person_reg_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='reg_status',
            field=models.CharField(blank=True, default='None', max_length=20, null=True, verbose_name='Status'),
        ),
    ]
