# Generated by Django 3.2.15 on 2022-11-24 13:26

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dormitory', '0065_alter_occupant_end_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='service',
        ),
        migrations.AlterField(
            model_name='bill_details',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))]),
        ),
        migrations.AlterField(
            model_name='bill_details',
            name='description',
            field=models.CharField(blank=True, default='None', max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))]),
        ),
        migrations.AlterField(
            model_name='service',
            name='base_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))]),
        ),
    ]
