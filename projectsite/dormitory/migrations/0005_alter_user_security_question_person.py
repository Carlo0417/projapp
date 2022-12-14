# Generated by Django 4.1 on 2022-08-27 15:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dormitory', '0004_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='security_question',
            field=models.CharField(choices=[('In what city were you born?', 'In what city were you born?'), ('What is the name of your favorite pet?', 'What is the name of your favorite pet?'), ('What is your mothers maiden name?', 'What is your mothers maiden name?'), ('What high school did you attend?', 'What high school did you attend?'), ('What was the name of your elementary school?', 'What was the name of your elementary school?'), ('What was your favorite food as a child?', 'What was your favorite food as a child?'), ('What year was your father (or mother) born?', 'What year was your father (or mother) born?')], max_length=250),
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('office_dept', models.CharField(choices=[('Computer Studies Department', 'Computer Studies Department'), ('Math Department', 'Math Department'), ('Science Department', 'Science Department'), ('Physical Education Department', 'Physical Education Department')], max_length=250)),
                ('program', models.CharField(choices=[('BSIT', 'BSIT'), ('BSCS', 'BSCS'), ('BSM', 'BSM'), ('BSS', 'BSS'), ('BSPE', 'BSPE'), ('NULL', 'NULL')], max_length=250)),
                ('rank', models.CharField(choices=[('Instructor I', 'Instructor I'), ('Instructor II', 'Instructor II'), ('Instructor III', 'Instructor III'), ('Instructor IV', 'Instructor IV'), ('Instructor V', 'Instructor V'), ('NULL', 'NULL')], max_length=50)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Rather not to say', 'Rather not to say')], max_length=50)),
                ('user_type', models.CharField(choices=[('Occupant', 'Occupant'), ('Admin', 'Admin')], max_length=50)),
                ('guardian', models.CharField(max_length=250)),
                ('contact_no', models.CharField(max_length=20)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dormitory.user')),
            ],
            options={
                'verbose_name_plural': 'Persons',
            },
        ),
    ]
