from django.db import models
from django.db.models.signals import post_save
# Create your models here.
from django.dispatch import receiver


class Student(models.Model):
    admission_number = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100)
    class_of_student = models.CharField(max_length=10)
    roll_number = models.IntegerField()
    percentage_of_mid1 = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    percentage_of_mid2 = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    percentage_of_final = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    student_image = models.ImageField(upload_to='student_image', default='user.jpeg')

    class Meta:
        db_table = 'Student'

    def __str__(self):
        return str(self.admission_number)


class Subjects(models.Model):
    subject_code = models.CharField(max_length=10, primary_key=True)
    subject_name = models.CharField(max_length=20)

    class Meta:
        db_table = 'Subjects'

    def __str__(self):
        return self.subject_name


class Class(models.Model):
    class_name = models.CharField(max_length=10, primary_key=True)

    class Meta:
        db_table = 'Class'

    def __str__(self):
        return self.class_name


class Marks(models.Model):
    admission_number = models.IntegerField()
    subject_code = models.CharField(max_length=10)
    mid1 = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    mid2 = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    final = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    subject_teacher = models.CharField(max_length=20, default='Not Assigned')

    class Meta:
        db_table = 'Marks'

    def __str__(self):
        return str(self.admission_number) + " " + self.subject_code


@receiver(post_save, sender=Marks)
def update_marks(sender, instance, created, **kwargs):
    if not created:
        subject_list = Marks.objects.filter(admission_number=instance.admission_number)
        student = Student.objects.get(admission_number=instance.admission_number)
        student.percentage_of_mid1 = calculate_percentage([subject.mid1 for subject in subject_list], 'm')
        student.percentage_of_mid2 = calculate_percentage([subject.mid2 for subject in subject_list], 'm')
        student.percentage_of_final = calculate_percentage([subject.final for subject in subject_list], 'f')
        student.save()


def calculate_percentage(list_of_subject, term):
    mul = 1
    if term == 'm':
        mul = 10
    percentage = 0
    for marks in list_of_subject:
        percentage += marks
    return (percentage * mul) / len(list_of_subject)
