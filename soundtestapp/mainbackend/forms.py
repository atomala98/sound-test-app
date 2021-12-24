from django import forms
from .models import Test, TestType

class RegisterForm(forms.Form):
    first_name = forms.CharField(label='First name', max_length=30)
    last_name = forms.CharField(label='Last name', max_length=30)
    start_date = forms.DateTimeField(label='Birth date', widget=forms.SelectDateWidget(years=(i for i in range(2015, 1899, -1))))
    gender = forms.ChoiceField(label='Gender', choices=[('M', 'M'), ('F', 'F')])


class AdminLoginForm(forms.Form):
    login = forms.CharField(label="Login", max_length=30)
    password = forms.CharField(label='Password', max_length=30, widget=forms.PasswordInput)
    

class CreateExam(forms.Form):
    exam_name = forms.CharField(label="Exam Name", max_length=30)
    test1 = forms.ModelChoiceField(label='Test', queryset=Test.objects.all())
    test1_type = forms.ModelChoiceField(label='Test type', queryset=TestType.objects.all())