# Generated by Django 3.2.15 on 2022-10-04 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dormitory', '0029_alter_bill_details_occupant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill_details',
            name='description',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]