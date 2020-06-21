from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from django.forms import formset_factory

from student.models import Student, Class, Marks
from teacher.models import ClassAndSubject

choice = (
    ('Nursery', 'Nursery'),
    ('L.K.G.', 'L.K.G.'),
    ('U.K.G.', 'U.K.G.'),
    ('I', 'I'),
    ('II', 'II'),
    ('III', 'III'),
    ('IV', 'IV'),
    ('V', 'V'),
    ('VI', 'VI'),
    ('VII', 'VII'),
    ('VIII', 'VIII'),
    ('IX', 'IX'),
    ('X', 'X'),
    ('XI', 'XI'),
    ('XII', 'XII'),
)


class AddStudentForm(forms.Form):
    admission_number = forms.CharField(max_length=10,
                                       label='Admission Number Of Student ',
                                       widget=forms.TextInput(attrs={
                                           'class': 'form-control',
                                           'placeholder': 'Admission Number',
                                           'style': 'background: rgba(251,252,250,0.33);border: none'
                                       }))

    name = forms.CharField(max_length=100,
                           label='Name Of Student',
                           widget=forms.TextInput(attrs={
                               'class': 'form-control',
                               'placeholder': 'Name',
                               'style': 'background: rgba(251,252,250,0.33);border: none'
                           }))

    class_of_student = forms.ChoiceField(choices=choice,
                                         label='Class',
                                         widget=forms.Select(attrs={
                                             'class': 'form-control',
                                             'placeholder': 'Class',
                                             'style': 'background: rgba(251,252,250,0.33);border: none'
                                         }
                                         ))

    roll_number = forms.IntegerField(label='Roll Number',
                                     widget=forms.NumberInput(attrs={
                                         'class': 'form-control',
                                         'placeholder': 'Roll Number',
                                         'style': 'background: rgba(251,252,250,0.33);border: none',
                                         'min': '1'
                                     }
                                     ))

    student_image = forms.ImageField(label='Student Image',
                                     widget=forms.FileInput(attrs={
                                         'class': 'form-control',
                                         'placeholder': 'Image',
                                         'style': 'background: rgba(251,252,250,0.33);border: none',
                                     }))

    def clean_admission_number(self):
        try:
            Student.objects.get(admission_number=self.cleaned_data['admission_number'])
            raise ValidationError('')
        except ValidationError:
            raise ValidationError('Student with Admission Number already exist.')
        except Exception:
            return self.cleaned_data['admission_number']

    def clean_class_of_student(self):
        try:
            class_name = Class.objects.get(class_name=self.cleaned_data['class_of_student'])
            if class_name:
                return self.cleaned_data['class_of_student']
        except Exception:
            raise ValidationError('No such class in school.')

    def clean_roll_number(self):
        return self.cleaned_data['roll_number']

    def clean_name(self):
        return self.cleaned_data['name']

    def clean_student_image(self):
        picture = self.cleaned_data['student_image']
        if not picture:
            raise ValidationError("No image!")
        else:
            w, h = get_image_dimensions(picture)
            if w > 450:
                raise ValidationError("Upload a max of 450px wide photo")
            if h > 450:
                raise ValidationError("Upload a photo of max height 450px")
        return picture

    def save(self):
        auth_user = User.objects.create_user(username=self.cleaned_data['admission_number'], password='9812')
        auth_user.save()

        student = Student(admission_number=self.cleaned_data['admission_number'],
                          name=self.cleaned_data['name'],
                          class_of_student=self.cleaned_data['class_of_student'],
                          roll_number=self.cleaned_data['roll_number'],
                          student_image=self.cleaned_data['student_image']
                          )
        student.save()

        list_of_subjects = ClassAndSubject.objects.filter(class_name=self.cleaned_data['class_of_student'])
        for subject in list_of_subjects:
            object = Marks.objects.create(admission_number=self.cleaned_data['admission_number'],
                                          subject_code=subject.subject_code)
            object.save()

        return student


class UpdationForm(forms.Form):
    admission_number = forms.CharField(max_length=10,
                                       widget=forms.TextInput(attrs={
                                           'hidden': ''
                                       }))
    name = forms.CharField(max_length=100,
                           label='Name',
                           widget=forms.TextInput(attrs={
                               'class': 'form-control',
                               'placeholder': 'Name',
                               'style': 'background: rgba(251,252,250,0.33);border: none'
                           }))

    class_of_student = forms.ChoiceField(choices=choice,
                                         label='Class',
                                         widget=forms.Select(attrs={
                                             'class': 'form-control',
                                             'placeholder': 'Class',
                                             'style': 'background: rgba(251,252,250,0.33);border: none'
                                         }
                                         ))
    roll_number = forms.IntegerField(label='Roll Number',
                                     widget=forms.NumberInput(attrs={
                                         'class': 'form-control',
                                         'placeholder': 'Roll Number',
                                         'style': 'background: rgba(251,252,250,0.33);border: none',
                                         'min': '1'
                                     }
                                     ))

    student_image = forms.ImageField(label='Student Image',
                                     widget=forms.FileInput(attrs={
                                         'class': 'form-control',
                                         'placeholder': 'Image',
                                         'style': 'background: rgba(251,252,250,0.33);border: none'
                                     }), required=False)

    def clean_student_image(self):
        picture = self.cleaned_data['student_image']
        if not picture:
            return self.cleaned_data['student_image']
        else:
            w, h = get_image_dimensions(picture)
            if w > 450:
                raise ValidationError("Upload a max of 450px wide photo")
            if h > 450:
                raise ValidationError("Upload a photo of max height 450px")
        return self.cleaned_data['student_image']


class SubjectForm(forms.Form):
    subject_code = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                                 'placeholder': 'Subject Code',
                                                                 'readonly': ''
                                                                 }))

    mid1 = forms.DecimalField(max_digits=5, decimal_places=2, max_value=10, min_value=0,
                              widget=forms.NumberInput(attrs={'class': 'form-control'}))
    mid2 = forms.DecimalField(max_digits=5, decimal_places=2, max_value=10, min_value=0,
                              widget=forms.NumberInput(attrs={'class': 'form-control'}))
    final = forms.DecimalField(max_digits=5, decimal_places=2, max_value=100, min_value=0,
                               widget=forms.NumberInput(attrs={'class': 'form-control'}))
    subject_teacher = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))


Formset = formset_factory(SubjectForm, extra=0)
