# Generated by Django 3.2.15 on 2022-12-14 02:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dormitory', '0076_alter_user_user_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('lastname', models.CharField(max_length=100)),
                ('firstname', models.CharField(max_length=100)),
                ('username', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
                ('security_question', models.CharField(blank=True, choices=[('In what city were you born?', 'In what city were you born?'), ('What is the name of your favorite pet?', 'What is the name of your favorite pet?'), ('What is your mothers maiden name?', 'What is your mothers maiden name?'), ('What high school did you attend?', 'What high school did you attend?'), ('What was the name of your elementary school?', 'What was the name of your elementary school?'), ('What was your favorite food as a child?', 'What was your favorite food as a child?'), ('What year was your father (or mother) born?', 'What year was your father (or mother) born?')], max_length=250, null=True)),
                ('security_answer', models.CharField(blank=True, max_length=250, null=True)),
                ('recovery_email', models.CharField(blank=True, max_length=250, null=True)),
                ('admin_class', models.CharField(blank=True, choices=[('Front Desk', 'Front Desk'), ('Accounting Staff', 'Accounting Staff'), ('Super Administrator', 'Super Administrator')], max_length=20, null=True)),
            ],
            options={
                'verbose_name_plural': 'Admins',
            },
        ),
    ]
