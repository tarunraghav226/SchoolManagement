# Create your views here.
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from student.models import Student, Subjects, Marks
from teacher.forms import AddStudentForm, UpdationForm, Formset
from teacher.models import Teacher, Teaches


def home(request):
    context = {'user_detail': Teacher.objects.get(teacher_id=request.user.username)}
    return render(request, 'teacher/home-dashboard.html', context)


def analytic_dashboard(request):
    context = {'user_detail': Teacher.objects.get(teacher_id=request.user.username)}
    if context['user_detail'].class_teacher_of != 'none':
        context['students_in_class'] = Student.objects.filter(class_of_student=context['user_detail'].class_teacher_of) \
            .order_by('name')
    return render(request, 'teacher/analytic-dashboard.html', context)


def details(request):
    context = {'user_detail': Teacher.objects.get(teacher_id=request.user.username)}
    subject_list = []
    for value in Teaches.objects.filter(teacher_id=request.user.username):
        subject_list.append(Subjects.objects.get(subject_code=value.subject_code).subject_name)
    context['teaches'] = subject_list
    return render(request, 'teacher/details-dashboard.html', context)


def add(request):
    context = {'user_detail': Teacher.objects.get(teacher_id=request.user.username), 'form': AddStudentForm()}
    return render(request, 'teacher/add-student.html', context)


def add_new_student(request):
    form = AddStudentForm(request.POST, request.FILES)
    context = {'user_detail': Teacher.objects.get(teacher_id=request.user.username), 'form': form}
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


def generateListOfSubjectWithMarks(adm_no):
    l = [{'subject_code': subject.subject_code,
          'mid1': subject.mid1,
          'mid2': subject.mid2,
          'final': subject.final,
          'subject_teacher': subject.subject_teacher} for subject in Marks.objects.filter(admission_number=adm_no)]
    return l


def search(request, adm_no=0):
    context = {'user_detail': Teacher.objects.get(teacher_id=request.user.username)}
    if adm_no == 0 and request.GET.get('id') is None:
        context['search'] = ''
    else:
        if request.GET.get('id') is not None:
            adm_no = request.GET.get('id')
        search_result = Student.objects.get(admission_number=adm_no)
        form = UpdationForm(initial={'admission_number': search_result.admission_number,
                                     'name': search_result.name,
                                     'class_of_student': search_result.class_of_student,
                                     'roll_number': search_result.roll_number,
                                     'student_image': search_result.student_image,
                                     })
        context['search'] = form

        list_of_subjects_details = generateListOfSubjectWithMarks(adm_no)
        context['alpha'] = Formset(initial=list_of_subjects_details)
    return render(request, 'teacher/search-dashboard.html', context)


def update(request):
    if request.method == "POST":
        updationForm = UpdationForm(request.POST, request.FILES)
        updationFormSet = Formset(request.POST)

        if updationForm.is_valid() and updationFormSet.is_valid():

            if updationForm.cleaned_data['student_image'] is not None:
                Student.objects.get(
                    admission_number=updationForm.cleaned_data['admission_number']).student_image.delete()
                Student.objects.filter(admission_number=updationForm.cleaned_data['admission_number']) \
                    .update(name=updationForm.cleaned_data['name'],
                            class_of_student=updationForm.cleaned_data['class_of_student'],
                            roll_number=updationForm.cleaned_data['roll_number'])
                student = Student.objects.get(admission_number=updationForm.cleaned_data['admission_number'])
                student.student_image = updationForm.cleaned_data['student_image']
                student.save()
            else:
                Student.objects.filter(admission_number=updationForm.cleaned_data['admission_number']). \
                    update(name=updationForm.cleaned_data['name'],
                           class_of_student=updationForm.cleaned_data['class_of_student'],
                           roll_number=updationForm.cleaned_data['roll_number'])

            for form in updationFormSet:
                Marks.objects.filter(admission_number=updationForm.cleaned_data['admission_number'],
                                     subject_code=form.cleaned_data['subject_code']) \
                    .update(mid1=form.cleaned_data['mid1'],
                            mid2=form.cleaned_data['mid2'],
                            final=form.cleaned_data['final'],
                            subject_teacher=form.cleaned_data['subject_teacher']
                            )
            messages.info(request, 'Success')
        else:
            context = {'user_detail': Teacher.objects.get(teacher_id=request.user.username), 'search': updationForm,
                       'alpha': updationFormSet}
            return render(request, 'teacher/search-dashboard.html', context)

    return redirect('/teacher/search/')


def delete(request):
    user_id = request.POST['id']
    Marks.objects.filter(admission_number=user_id).delete()
    User.objects.get(username=user_id).delete()
    Student.objects.get(admission_number=user_id).delete()
    return redirect('/teacher/analytic-dashboard/')
