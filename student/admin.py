from django.contrib import admin

from student.models import Class
from student.models import Marks
from student.models import Student
from student.models import Subjects

# Register your models here.

admin.site.register(Student)
admin.site.register(Subjects)
admin.site.register(Class)
admin.site.register(Marks)
