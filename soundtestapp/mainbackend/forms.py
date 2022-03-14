from django import forms
from .models import Test, TestType, Fileset
from django.forms import ValidationError

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
    
    def __init__(self, amount, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i in range(1, amount + 1):
            self.fields[f"test_{i}"] = forms.ModelChoiceField(label=f'Test {i}', queryset=Test.objects.all())


class AddFilesForm(forms.Form):
    fileset_name = forms.CharField(label="Fileset name", max_length=30)
    fileset_type = forms.ChoiceField(label='Fileset type', choices=[
        ('One', 'One file fileset'),
        ('Two', 'Two file fileset'),
        ('MUSHRA', 'MUSHRA Fileset')])
    amount = forms.IntegerField(label='Files Amount')
    
    
class OneFileUploadForm(forms.Form):    
    def __init__(self, amount, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.amount = amount
        for i in range(1, amount + 1):
            self.fields[f"file{i}"] = forms.FileField(label=f"File {i}:")
            self.fields[f"file_label{i}"] = forms.CharField(label=f"File {i} Label:", max_length=30)
    
    
    def clean(self):
         for i in range(1, self.amount + 1):
            file = self.cleaned_data[f'file{i}']
            if file.size > 10000000:
                raise ValidationError("File too large")
            if file.name.split('.')[1] != "mp3" and file.name.split('.')[1] != "wav":
                raise ValidationError("Wrong file format")
    
    
class TwoFilesUploadForm(forms.Form):
    def __init__(self, amount, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.amount = amount
        for i in range(1, amount + 1):
            self.fields[f"file_A{i}"] = forms.FileField(label=f"File {i}A:")
            self.fields[f"file_label_A{i}"] = forms.CharField(label=f"File {i}A Label:", max_length=30)
            self.fields[f"file_B{i}"] = forms.FileField(label=f"File {i}B:")
            self.fields[f"file_label_B{i}"] = forms.CharField(label=f"File {i}B Label:", max_length=30)
            
    def clean(self):
        for i in range(1, self.amount + 1):
            file = self.cleaned_data[f'file_A{i}']
            if file.size > 10000000:
                raise ValidationError("File too large")
            if file.name.split('.')[1] != "mp3" and file.name.split('.')[1] != "wav":
                raise ValidationError("Wrong file format")
            file = self.cleaned_data[f'file_B{i}']
            if file.size > 10000000:
                raise ValidationError("File too large")
            if file.name.split('.')[1] != "mp3" and file.name.split('.')[1] != "wav":
                raise ValidationError("Wrong file format")
    
    
class MUSHRATestUpload(forms.Form):
    original_file = forms.FileField()
    original_file_label = forms.CharField(label="Original File Label", max_length=30)
    
    def clean(self):
        original_file = self.cleaned_data['original_file']
        if original_file.size > 10000000:
            raise ValidationError("File too large")
        if original_file.name.split('.')[1] != "mp3" and original_file.name.split('.')[1] != "wav":
            raise ValidationError("Wrong file format")
        
        
class FrequencyDifferenceParameters(forms.Form):
    def __init__(self, number, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[f'parameter_1_{number}'] = forms.ChoiceField(label='Method', choices=[
            ('C', 'Costant Stimuli'), 
            ('A', 'Adjustments')])
        self.fields[f'parameter_2_{number}'] = forms.FloatField(label="Step [Hz]")
        
        
class ACRParameters(forms.Form):
    def __init__(self, number, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[f'parameter_1_{number}'] = forms.ModelChoiceField(label=f'Fileset', queryset=Fileset.objects.filter(fileset_type="One File Set"))
        self.fields[f'parameter_2_{number}'] = forms.ChoiceField(label='Method', choices=[
            ('Normal', 'Normal'), 
            ('Random', 'Random'),
            ('Reversed', 'Reversed')])