# Generated by Django 3.2.15 on 2023-01-03 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dormitory', '0083_delete_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='office_dept',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Office / Department'),
        ),
    ]
