# Generated by Django 3.2.15 on 2023-01-02 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dormitory', '0079_auto_20230102_1714'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='person_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
