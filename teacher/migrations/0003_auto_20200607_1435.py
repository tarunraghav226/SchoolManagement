# Generated by Django 2.2.5 on 2020-06-07 14:35

from django.db import migrations, models

import teacher.models


class Migration(migrations.Migration):
    dependencies = [
        ('teacher', '0002_teacher_teacher_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='teacher_image',
            field=models.ImageField(default='user.jpeg', upload_to=teacher.models.user_directory_path),
        ),
    ]