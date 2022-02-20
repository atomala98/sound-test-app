from django import forms
from .models import Test, TestType

class RegisterForm(forms.Form):
    first_name = forms.CharField(label='First name', max_length=30)
    last_name = forms.CharField(label='Last name', max_length=30)
    birth_date = forms.DateTimeField(label='Birth date', widget=forms.SelectDateWidget(years=range(2015, 1899, -1)))
    gender = forms.ChoiceField(label='Gender', choices=[('M', 'M'), ('F', 'F')])


class AdminLoginForm(forms.Form):
    login = forms.CharField(label="Login", max_length=30)
    password = forms.CharField(label='Password', max_length=30, widget=forms.PasswordInput)
    

class CreateExam(forms.Form):
    exam_name = forms.CharField(label="Exam Name", max_length=30)
    test1 = forms.ModelChoiceField(label='Test', queryset=Test.objects.all())
    test1_type = forms.ModelChoiceField(label='Test type', queryset=TestType.objects.all())
    

class AddFilesForm(forms.Form):
    fileset_name = forms.CharField(label="Fileset name", max_length=30)
    fileset_type = forms.ChoiceField(label='Fileset type', choices=[('MUSHRA', 'MUSHRA Fileset')])
    
    
class MUSHRATestUpload(forms.Form):
    original_file = forms.FileField()
    original_file_label = forms.CharField(label="Original File Label", max_length=30)