# Generated by Django 3.2.15 on 2022-11-14 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dormitory', '0058_auto_20221107_1751'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill_details',
            name='quantity',
            field=models.CharField(default=0, max_length=5, verbose_name='Quantity'),
        ),
        migrations.AlterField(
            model_name='bed',
            name='price',
            field=models.DecimalField(choices=[(1500, 1500), (4500, 4500)], decimal_places=0, default=0, max_digits=6),
        ),
        migrations.AlterField(
            model_name='person',
            name='office_dept',
            field=models.CharField(choices=[('Department of Behavioral Science', 'Department of Behavioral Science'), ('Department of Social Sciences', 'Department of Social Sciences'), ('Department of Foreign Language', 'Department of Foreign Language'), ('Bio-Physical Science Department', 'Bio-Physical Science Department'), ('Computer Studies Department', 'Computer Studies Department'), ('Mathematics Department', 'Mathematics Department'), ('Department of Physical Education', 'Department of Physical Education'), ('Department of Elementary Education', 'Department of Elementary Education'), ('Department of Secondary Education', 'Department of Secondary Education'), ('Department of Accountancy', 'Department of Accountancy'), ('Department of Marketing Management, Entrepreneurship, and Public Administration', 'Department of Marketing Management, Entrepreneurship, and Public Administration'), ('Department of Financial Management, Human Resource Management, and Business Economics', 'Department of Financial Management, Human Resource Management, and Business Economics'), ('Hospitality Management Department', 'Hospitality Management Department'), ('Tourism Management Department', 'Tourism Management Department'), ('Department of Civil Engineering', 'Department of Civil Engineering'), ('Department of Mechanical Engineering', 'Department of Mechanical Engineering'), ('Department of Electrical Engineering', 'Department of Electrical Engineering'), ('Department of Petroleum Engineering', 'Department of Petroleum Engineering'), ('Department of Architecture', 'Department of Architecture'), ('Department of Nursing', 'Department of Nursing'), ('Department of Midwifery', 'Department of Midwifery'), ('Not yet included', 'Not yet included')], max_length=250, verbose_name='Office / Department'),
        ),
        migrations.AlterField(
            model_name='person',
            name='program',
            field=models.CharField(choices=[('Bachelor of Science in Social Work', 'Bachelor of Science in Social Work'), ('Bachelor of Science in Psychology', 'Bachelor of Science in Psychology'), ('Bachelor of Arts in Communication', 'Bachelor of Arts in Communication'), ('Bachelor of Arts in Political Science', 'Bachelor of Arts in Political Science'), ('Bachelor of Arts in Philippine Studies ', 'Bachelor of Arts in Philippine Studies '), ('Bachelor of Science in Biology Major in Medical Biology', 'Bachelor of Science in Biology Major in Medical Biology'), ('Bachelor of Science in Marine Biology', 'Bachelor of Science in Marine Biology'), ('Bachelor of Science in Environmental Science', 'Bachelor of Science in Environmental Science'), ('Bachelor of Science in Information Technology', 'Bachelor of Science in Information Technology'), ('Bachelor of Science in Computer Science', 'Bachelor of Science in Computer Science'), ('Bachelor of Science in Physical Education', 'Bachelor of Science in Physical Education'), ('Bachelor of Science in Elementary Education', 'Bachelor of Science in Elementary Education'), ('Bachelor of Science in Secondary Education Major in Science', 'Bachelor of Science in Secondary Education Major in Science'), ('Bachelor of Science in Secondary Education Major in Math', 'Bachelor of Science in Secondary Education Major in Math'), ('Bachelor of Science in Secondary Education Major in English', 'Bachelor of Science in Secondary Education Major in English'), ('Bachelor of Science in Secondary Education Major in Filipino', 'Bachelor of Science in Secondary Education Major in Filipino'), ('Bachelor of Science in Secondary Education Major in Social Studies', 'Bachelor of Science in Secondary Education Major in Social Studies'), ('Bachelor of Science in Secondary Education Major in Values', 'Bachelor of Science in Secondary Education Major in Values'), ('Bachelor of Science in Accountancy', 'Bachelor of Science in Accountancy'), ('Bachelor of Science in Management Accountancy', 'Bachelor of Science in Management Accountancy'), ('Bachelor of Science in Entrepreneurship', 'Bachelor of Science in Entrepreneurship'), ('Bachelor of Science in Business Administration  Major in Marketing Management ', 'Bachelor of Science in Business Administration  Major in Marketing Management '), ('Bachelor of Science in Business Administration  Major in Human Resource Management', 'Bachelor of Science in Business Administration  Major in Human Resource Management'), ('Bachelor of Science in Hospitality Management', 'Bachelor of Science in Hospitality Management'), ('Track - Culinary Arts and Kitchen Management', 'Track - Culinary Arts and Kitchen Management'), ('Bachelor of Science in Tourism Management', 'Bachelor of Science in Tourism Management'), ('Track - Hotel,Resort, and Club Management', 'Track - Hotel,Resort, and Club Management'), ('Bachelor of Science in Civil Engineering', 'Bachelor of Science in Civil Engineering'), ('Bachelor of Science in Mechanical Engineering', 'Bachelor of Science in Mechanical Engineering'), ('Bachelor of Science in Electrical Engineering', 'Bachelor of Science in Electrical Engineering'), ('Bachelor of Science in Petroleum Engineering', 'Bachelor of Science in Petroleum Engineering'), ('Bachelor of Science in Architecture', 'Bachelor of Science in Architecture'), ('Bachelor of Science in Nursing', 'Bachelor of Science in Nursing'), ('Diploma in Midwifery', 'Diploma in Midwifery'), ('Bachelor of Science in Midwifery', 'Bachelor of Science in Midwifery'), ('Bachelor of Science in Criminology', 'Bachelor of Science in Criminology')], max_length=250),
        ),
    ]
