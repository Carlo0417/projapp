# Generated by Django 3.2.15 on 2023-04-06 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dormitory', '0089_auto_20230406_0033'),
    ]

    operations = [
        migrations.RenameField(
            model_name='occupantdemerit',
            old_name='remarks',
            new_name='prev_remarks',
        ),
        migrations.AddField(
            model_name='occupantdemerit',
            name='new_remarks',
            field=models.TextField(blank=True, default='', max_length=500, null=True),
        ),
    ]
