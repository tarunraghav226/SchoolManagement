from django.db import models

# Create your models here.


class Student(models.Model):
    admission_number = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    class_of_student = models.CharField(max_length=10)
    roll_number = models.IntegerField()
    percentage = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        db_table = 'Student'

    def __str__(self):
        return self.admission_number
