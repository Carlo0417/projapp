# Generated by Django 3.2.15 on 2022-10-18 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dormitory', '0044_alter_bed_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='gender',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('LGBTQ+', 'LGBTQ+')], max_length=50),
        ),
    ]
