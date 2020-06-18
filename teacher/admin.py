# Register your models here.
from django.contrib import admin

from teacher.models import Teacher, Teaches, ClassAndSubject

admin.site.register(Teacher)
admin.site.register(Teaches)
admin.site.register(ClassAndSubject)
