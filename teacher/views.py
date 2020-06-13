# Create your views here.
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from student.models import Student, Subjects, Marks
from teacher.forms import AddStudentForm
from teacher.models import Teacher, Teaches


def home(request):
    context = {}
    context['user_detail'] = Teacher.objects.get(teacher_id=request.user.username)
    return render(request, 'teacher/home-dashboard.html', context)


def analytic_dashboard(request):
    context = {}
    context['user_detail'] = Teacher.objects.get(teacher_id=request.user.username)
    if context['user_detail'].class_teacher_of != 'none':
        context['students_in_class'] = Student.objects.filter(class_of_student=context['user_detail'].class_teacher_of) \
            .order_by('name')
    return render(request, 'teacher/analytic-dashboard.html', context)


def details(request):
    context = {}
    context['user_detail'] = Teacher.objects.get(teacher_id=request.user.username)
    subject_list = []
    for value in Teaches.objects.filter(teacher_id=request.user.username):
        subject_list.append(Subjects.objects.get(subject_code=value.subject_code).subject_name)
    context['teaches'] = subject_list
    return render(request, 'teacher/details-dashboard.html', context)


def add(request):
    context = {}
    context['user_detail'] = Teacher.objects.get(teacher_id=request.user.username)
    context['form'] = AddStudentForm()
    return render(request, 'teacher/add-student.html', context)


def search(request):
    context = {}
    context['user_detail'] = Teacher.objects.get(teacher_id=request.user.username)
    return render(request, 'teacher/search-dashboard.html', context)


def add_new_student(request):
    form = AddStudentForm(request.POST, request.FILES)
    context = {}
    context['user_detail'] = Teacher.objects.get(teacher_id=request.user.username)
    context['form'] = form
    if request.method == 'POST':
        if form.is_valid():
            messages.info(request, "Student (" + str(form.cleaned_data['admission_number']) + ") is added.")
            form.save()
            context['form'] = AddStudentForm()
            return render(request, 'teacher/add-student.html', context)
    else:
        messages.info(request, 'Student Admission Number - Not added')
        return render(request, 'teacher/add-student.html', context)
    return render(request, 'teacher/add-student.html', context)


def delete(request):
    user_id = request.POST['id']
    Marks.objects.filter(admission_number=user_id).delete()
    User.objects.get(username=user_id).delete()
    Student.objects.get(admission_number=user_id).delete()
    return redirect('/teacher/analytic-dashboard/')
