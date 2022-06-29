from django import forms
from .models import Test, TestType, Fileset
from django.forms import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator

class RegisterForm(forms.Form):
    first_name = forms.CharField(label='First name', max_length=30)
    last_name = forms.CharField(label='Last name', max_length=30)
    birth_date = forms.DateTimeField(label='Birth date', widget=forms.SelectDateWidget(years=range(2015, 1899, -1)))
    gender = forms.ChoiceField(label='Gender', choices=[('M', 'M'), ('F', 'F')])


class AdminLoginForm(forms.Form):
    login = forms.CharField(label="Login", max_length=30)
    password = forms.CharField(label='Password', max_length=30, widget=forms.PasswordInput)
    

class CreateExamAmount(forms.Form):
    test_amount = forms.IntegerField(label="Tests amount")


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
    original_file = forms.FileField(label=f"Original File:")
    
    def __init__(self, amount, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.amount = amount
        for i in range(1, amount + 1):
            self.fields[f"file{i}"] = forms.FileField(label=f"File {i}: ")
            self.fields[f"file_label{i}"] = forms.CharField(label=f"File {i} Label: ", max_length=30)
    
    def clean(self):
         for i in range(1, self.amount + 1):
            file = self.cleaned_data[f'file{i}']
            if file.size > 10000000:
                raise ValidationError("File too large")
            if file.name.split('.')[1] != "mp3" and file.name.split('.')[1] != "wav":
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
        self.fields[f'parameter_2_{number}'] = forms.ChoiceField(label='Recording order', choices=[
            ('Normal', 'Normal'), 
            ('Random', 'Random'),
            ('Reversed', 'Reversed')])
        self.fields[f'parameter_3_{number}'] = forms.ChoiceField(label='Scale', choices=[
            ('Listening-quality scale', 'Listening-quality scale'), 
            ('Listening-effort scale', 'Listening-effort scale'),
            ('Loudness-preference scale', 'Loudness-preference scale')])
        
        
class ACRTest(forms.Form):
    def __init__(self, scale, *args, **kwargs):
        super().__init__(*args, **kwargs)
        possible_scales = {
            "Listening-quality scale": forms.ChoiceField(label='Rate quality of the recording', choices=[
            (5, 'Excellent'), 
            (4, 'Good'),
            (3, 'Fair'), 
            (2, 'Poor'),
            (1, 'Bads'),
            ]),
            "Listening-effort scale": forms.ChoiceField(label='Rate effort required to understand meaning of recording', choices=[
            (5, 'Complete relaxation possible; no effort required'), 
            (4, 'Attention necessary; no appreciable effort required'),
            (3, 'Moderate effort required'), 
            (2, 'Considerable effort required'),
            (1, 'No meaning understood with any feasible effort'),
            ]),
            "Loudness-preference scale": forms.ChoiceField(label='Rate loudness of recording', choices=[
            (5, 'Much louder than preferred'), 
            (4, 'Louder than preferred'),
            (3, 'Preferred'), 
            (2, 'Quieter than preferred'),
            (1, 'Much quieter than preferred'),
            ]),
        }
        self.fields['score'] = possible_scales[scale]
        
        
class DCRParameters(forms.Form):
    def __init__(self, number, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[f'parameter_1_{number}'] = forms.ModelChoiceField(label=f'Fileset', queryset=Fileset.objects.filter(fileset_type="Two File Set"))
        self.fields[f'parameter_2_{number}'] = forms.ChoiceField(label='Recording order', choices=[
            ('Normal', 'Normal'), 
            ('Random', 'Random'),
            ('Reversed', 'Reversed')])
        self.fields[f'parameter_3_{number}'] = forms.ChoiceField(label='Stimulus presentation', choices=[
            ('Pairs', 'Pairs'), 
            ('Repeated pairs', 'Repeated pairs')])
        
        
class DCRTest(forms.Form):
    score = forms.ChoiceField(label='Rate recording degradation', choices=[
            (5, 'Degradation is inaudible'), 
            (4, 'Degradation is audible but not annoying'),
            (3, 'Degradation is slightly annoying'), 
            (2, 'Degradation is annoying'),
            (1, 'Degradation is very annoying'),
            ])  


class CCRParameters(forms.Form):
    def __init__(self, number, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[f'parameter_1_{number}'] = forms.ModelChoiceField(label=f'Fileset', queryset=Fileset.objects.filter(fileset_type="Two File Set"))
        self.fields[f'parameter_2_{number}'] = forms.ChoiceField(label='Recording order', choices=[
            ('Normal', 'Normal'), 
            ('Random', 'Random'),
            ('Reversed', 'Reversed')])
        self.fields[f'parameter_3_{number}'] = forms.ChoiceField(label='Stimulus presentation', choices=[
            ('Pairs', 'Pairs'), 
            ('Repeated pairs', 'Repeated pairs')])
        
        
class CCRTest(forms.Form):
    score = forms.ChoiceField(label='The Quality of the Second Compared to the Quality of the First is:', choices=[
            (3, 'Much Better'), 
            (2, 'Better'),
            (1, 'Slightly Better'), 
            (0, 'About the Same'),
            (-1, 'Slightly Worse'),
            (-2, 'Worse'),
            (-3, 'Much Worse'),
            ])


class MUSHRAParameters(forms.Form):
    def __init__(self, number, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[f'parameter_1_{number}'] = forms.ModelChoiceField(label=f'Fileset', queryset=Fileset.objects.filter(fileset_type="MUSHRA Set"))

    
class MUSHRATest(forms.Form):
    def __init__(self, number, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i in range(1, number + 1):
            self.fields[f'result_{i}'] = forms.IntegerField(label='Rate recording: ', min_value=1, max_value=100)
            
            
class ABXParameters(forms.Form):
    def __init__(self, number, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[f'parameter_1_{number}'] = forms.ModelChoiceField(label=f'Fileset', queryset=Fileset.objects.filter(fileset_type="Two File Set"))


class ABXTest(forms.Form):
    score = forms.ChoiceField(label='Third recording is the same as:', choices=[
            (1, 'First one'),
            (-1, 'Second one'), 
            ])
    
class ABCHRParameters(forms.Form):
    def __init__(self, number, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[f'parameter_1_{number}'] = forms.ModelChoiceField(label=f'Fileset', queryset=Fileset.objects.filter(fileset_type="Two File Set"))


class ABCHRTest(forms.Form):
    first_score = forms.DecimalField(label=f'Rate first recording compared to reference', max_digits=5, decimal_places=1, validators=[MinValueValidator(1),
                                       MaxValueValidator(5)])
    second_score = forms.DecimalField(label=f'Rate second recording compared to reference', max_digits=5, decimal_places=1, validators=[MinValueValidator(1),
                                       MaxValueValidator(5)])
    
class JoinExamForm(forms.Form):
    inv_code = forms.CharField(label="Invitation code", max_length=8, min_length=8)