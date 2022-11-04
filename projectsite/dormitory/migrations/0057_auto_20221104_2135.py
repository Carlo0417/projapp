# Generated by Django 3.2.15 on 2022-11-04 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dormitory', '0056_person_reg_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='Field3',
            field=models.BooleanField(default=False, verbose_name='Fully accomplished application form (form OIA-OID)'),
        ),
        migrations.AlterField(
            model_name='person',
            name='address',
            field=models.CharField(default='', max_length=250, verbose_name='Address'),
        ),
        migrations.AlterField(
            model_name='person',
            name='city',
            field=models.CharField(default='Puerto Princesa City', max_length=250, verbose_name='City'),
        ),
        migrations.AlterField(
            model_name='person',
            name='contact_no',
            field=models.CharField(default='', max_length=20, verbose_name='Contact Number'),
        ),
        migrations.AlterField(
            model_name='person',
            name='first_name',
            field=models.CharField(default='', max_length=250),
        ),
        migrations.AlterField(
            model_name='person',
            name='guardian_contact_no',
            field=models.CharField(default='', max_length=20, verbose_name="Guardian's Contact Number"),
        ),
        migrations.AlterField(
            model_name='person',
            name='guardian_email_address',
            field=models.EmailField(default='', max_length=250, verbose_name="Guardian's Email"),
        ),
        migrations.AlterField(
            model_name='person',
            name='guardian_first_name',
            field=models.CharField(default='', max_length=250, verbose_name="Guardian's First name"),
        ),
        migrations.AlterField(
            model_name='person',
            name='guardian_last_name',
            field=models.CharField(default='', max_length=250, verbose_name="Guardian's Last name"),
        ),
        migrations.AlterField(
            model_name='person',
            name='guardian_present_address',
            field=models.CharField(default='', max_length=250, verbose_name="Guardian's Address"),
        ),
        migrations.AlterField(
            model_name='person',
            name='last_name',
            field=models.CharField(default='', max_length=250),
        ),
        migrations.AlterField(
            model_name='person',
            name='middle_name',
            field=models.CharField(blank=True, default='', max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='psu_email',
            field=models.EmailField(default='', max_length=250, verbose_name='PSU Email'),
        ),
    ]