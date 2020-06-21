from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from student.forms import LoginForm
from teacher.models import Teacher


def login_page(request):
    if request.user.is_authenticated:
        try:
            Teacher.objects.get(teacher_id=request.user.username)
            return redirect('/teacher/home/')
        except:
            return redirect('/student/home/')
    else:
        login_form = LoginForm()
        context = {'login_form': login_form}
        return render(request, 'login.html', context)


def login_user(request):
    if request.user.is_authenticated:
        try:
            Teacher.objects.get(teacher_id=request.user.username)
            return redirect('/teacher/home/')
        except:
            return redirect('/student/home/')
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['id'], password=form.cleaned_data['password'])
            if user:
                login(request, user)

                if form.cleaned_data['login_as'] == 'Student':
                    return redirect('/student/home/')

                if form.cleaned_data['login_as'] == 'Teacher':
                    return redirect('/teacher/home/')
            else:
                messages.info(request, "No user found")
                return render(request, 'login.html', {'login_form': form})
        else:
            return render(request, 'login.html', {'login_form': form})


@login_required
def logout_user(request):
    logout(request)
    return redirect('/')
