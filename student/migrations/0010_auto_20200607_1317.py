# Generated by Django 2.2.5 on 2020-06-07 13:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('student', '0009_auto_20200607_1316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='student_image',
            field=models.ImageField(default='user.jpeg', height_field=400, upload_to='student_image', width_field=400),
        ),
    ]