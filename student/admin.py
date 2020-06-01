from django.contrib import admin

from student.models import Student
from student.models import Subjects

# Register your models here.

admin.site.register(Student)
admin.site.register(Subjects)
