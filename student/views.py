from django.shortcuts import render

# Create your views here.
from student.models import Student, Marks, Subjects


def dashboard(request):
    context = {}
    context['user_detail'] = Student.objects.get(admission_number=request.user.username)
    return render(request, 'student/home-dashboard.html', context)


def analytic_dashboard(request):
    context = {}
    context['user_detail'] = Student.objects.get(admission_number=request.user.username)
    context['subjects'] = Marks.objects.filter(admission_number=request.user.username)
    return render(request, 'student/analytic-dashboard.html', context)


def details(request):
    context = {}
    context['user_detail'] = Student.objects.get(admission_number=request.user.username)
    subject_name = []
    for i in Marks.objects.filter(admission_number=request.user.username):
        subject_name.append(Subjects.objects.get(subject_code=i.subject_code).subject_name)
    context['subjects'] = subject_name
    return render(request, 'student/details-dashboard.html', context)


def search(request):
    context = {}
    context['user_detail'] = Student.objects.get(admission_number=request.user.username)
    context['search'] = ''
    return render(request, 'student/search-dashboard.html', context)


def get_result(request):
    context = {}
    context['search'] = ''
    context['user_detail'] = Student.objects.get(admission_number=request.user.username)
    try:
        object = Student.objects.get(admission_number=request.GET.get(key='id'))
        subject_name = []
        for i in Marks.objects.filter(admission_number=request.GET.get(key='id')):
            subject_name.append(Subjects.objects.get(subject_code=i.subject_code).subject_name)
        context['subjects'] = subject_name
        context['search'] = object
    except Exception:
        context['search'] = "user_not_found_404"
    return render(request, 'student/search-dashboard.html', context)


def add(request):
    return render(request, 'head/add-teacher.html')
