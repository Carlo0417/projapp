# Generated by Django 3.2.15 on 2022-10-04 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dormitory', '0026_alter_occupant_bedprice'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='boarder_type',
            field=models.CharField(choices=[('Local', 'Local'), ('Foreign', 'Foreign')], default='Local', max_length=50),
        ),
    ]
