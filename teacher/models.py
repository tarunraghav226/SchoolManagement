# Create your models here.
from django.db import models


class Teacher(models.Model):
    teacher_id = models.CharField(max_length=10, primary_key=True)
    teacher_name = models.CharField(max_length=100)
    class_teacher_of = models.CharField(max_length=10)
    teacher_image = models.ImageField(upload_to='teacher', default='user.jpeg')

    class Meta:
        db_table = 'Teacher'

    def __str__(self):
        return self.teacher_name + ' ' + self.id


class Teaches(models.Model):
    teacher_id = models.CharField(max_length=10)
    subject_code = models.CharField(max_length=10)

    class Meta:
        db_table = 'Teaches'

    def __str__(self):
        return self.id + ' ' + self.subject_code
