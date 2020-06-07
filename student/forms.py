from django import forms
from django.core.exceptions import ValidationError

from student.models import Student

choice = (('Head', 'Head'), ('Teacher', 'Teacher'), ('Student', 'Student'))


class LoginForm(forms.Form):
    login_as = forms.ChoiceField(choices=choice, widget=forms.Select(
        attrs={'class': 'form-control'}))

    id = forms.CharField(max_length=10, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'ID'}))

    password = forms.CharField(max_length=10,
                               widget=forms.PasswordInput(
                                   attrs={'placeholder': 'Enter Password',
                                          'class': 'form-control',
                                          'label': 'Password'}))

    def clean_login_as(self):
        return self.cleaned_data['login_as']

    def clean_id(self):
        try:
            student = Student.objects.get(admission_number=self.id)
        except Exception:
            return self.cleaned_data['id']
            raise ValidationError('Not registered')

        return self.cleaned_data['id']

    def clean_password(self):
        return self.cleaned_data['password']
