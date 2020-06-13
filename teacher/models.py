# Create your models here.
from django.db import models


def user_directory_path(instance, filename):
    return 'teacher/{0}/{1}'.format(instance.teacher_id, instance.teacher_name + filename)


class Teacher(models.Model):
    teacher_id = models.CharField(max_length=10, primary_key=True)
    teacher_name = models.CharField(max_length=100)
    class_teacher_of = models.CharField(max_length=10, default='none')
    teacher_image = models.ImageField(upload_to=user_directory_path, default='user.jpeg')

    class Meta:
        db_table = 'Teacher'

    def __str__(self):
        return self.teacher_name + ' ' + self.teacher_id


class Teaches(models.Model):
    teacher_id = models.CharField(max_length=10)
    subject_code = models.CharField(max_length=10)

    class Meta:
        db_table = 'Teaches'

    def __str__(self):
        return self.teacher_id + ' ' + self.subject_code


class ClassAndSubject(models.Model):
    class_name = models.CharField(max_length=10)
    subject_code = models.CharField(max_length=10)

    def __str__(self):
        return 'Class-> ' + self.class_name + ' Subject Code-> ' + self.subject_code;

    class Meta:
        db_table = 'ClassAndSubject'
