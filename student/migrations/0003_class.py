# Generated by Django 2.2.5 on 2020-06-01 08:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('student', '0002_subjects'),
    ]

    operations = [
        migrations.CreateModel(
            name='Class',
            fields=[
                ('class_name', models.CharField(max_length=10, primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'Class',
            },
        ),
    ]