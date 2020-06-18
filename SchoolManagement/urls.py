"""SchoolManagement URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from SchoolManagement import views, settings
from student import views as std_view
from teacher import views as teacher_view

urlpatterns = [
    path('admin/', admin.site.urls),
                  path('login/', views.login_user),
                  path('logout/', views.logout_user),
                  path('', views.login_page),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

studentpatterns = [
    path('student/analytic-dashboard/', std_view.analytic_dashboard),
    path('student/details/', std_view.details),
    path('student/search/', std_view.search),
    path('student/get_search_result/', std_view.get_result),
    path('student/home/', std_view.dashboard)]

teacherpatterns = [
    path('teacher/home/', teacher_view.home),
    path('teacher/analytic-dashboard/', teacher_view.analytic_dashboard),
    path('teacher/details/', teacher_view.details),
    path('teacher/add/', teacher_view.add),
    path('teacher/search/', teacher_view.search),
    path('teacher/add_new_student/', teacher_view.add_new_student),
    path('teacher/delete/', teacher_view.delete),
    url(r'^teacher\/search\/(?P<adm_no>\d+)\/$', teacher_view.search),
    path('teacher/update_student_data/', teacher_view.update)
]

urlpatterns += studentpatterns
urlpatterns += teacherpatterns
