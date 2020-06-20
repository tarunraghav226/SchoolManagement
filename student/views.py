from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from student.models import Student, Marks, Subjects
from teacher.models import Teacher, Teaches


@login_required
def dashboard(request):
    context = {'user_detail': Student.objects.get(admission_number=request.user.username)}
    return render(request, 'student/home-dashboard.html', context)


def calculate_percentage(list_of_subject):
    percentage = 0
    for marks in list_of_subject:
        percentage += marks
    return percentage / len(list_of_subject)


@login_required
def analytic_dashboard(request):
    context = {'user_detail': Student.objects.get(admission_number=request.user.username),
               'subjects': Marks.objects.filter(admission_number=request.user.username)}
    context['user_detail'].percentage_of_mid1 = calculate_percentage([subject.mid1 for subject in context['subjects']])
    context['user_detail'].percentage_of_mid2 = calculate_percentage([subject.mid2 for subject in context['subjects']])
    context['user_detail'].percentage_of_final = calculate_percentage(
        [subject.final for subject in context['subjects']])
    return render(request, 'student/analytic-dashboard.html', context)


@login_required
def details(request):
    context = {'user_detail': Student.objects.get(admission_number=request.user.username)}
    subject_name = []
    for i in Marks.objects.filter(admission_number=request.user.username):
        subject_name.append(Subjects.objects.get(subject_code=i.subject_code).subject_name)
    context['subjects'] = subject_name
    return render(request, 'student/details-dashboard.html', context)


@login_required
def search(request):
    context = {'user_detail': Student.objects.get(admission_number=request.user.username), 'search': ''}
    return render(request, 'student/search-dashboard.html', context)


@login_required
def get_result(request):
    context = {'search': '', 'user_detail': Student.objects.get(admission_number=request.user.username)}
    try:
        if request.GET.get('search_whom') == 'Student':
            context['searched_user'] = 'Student'
            student_object = Student.objects.get(admission_number=request.GET.get(key='id'))
            subject_name = []
            for i in Marks.objects.filter(admission_number=request.GET.get(key='id')):
                subject_name.append(Subjects.objects.get(subject_code=i.subject_code).subject_name)
            context['subjects'] = subject_name
            context['search'] = student_object
        else:
            context['searched_user'] = 'Teacher'
            teacher_object = Teacher.objects.get(teacher_id=request.GET.get('id'))
            subject_name = []
            for subject in Teaches.objects.filter(teacher_id=request.GET.get('id')):
                subject_name.append(Subjects.objects.get(subject_code=subject.subject_code).subject_name)
            print(subject_name)
            context['subjects'] = subject_name if subject_name != [] else 'none'

            context['search'] = teacher_object
    except Exception:
        context['search'] = "user_not_found_404"
    return render(request, 'student/search-dashboard.html', context)

