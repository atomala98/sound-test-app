from django import forms

class RegisterForm(forms.Form):
    first_name = forms.CharField(label='First name', max_length=30)
    last_name = forms.CharField(label='Last name', max_length=30)
    birth_date = forms.DateField(label='Birth date')
    gender = forms.ChoiceField(label='Gender', choices=[('M', 'M'), ('F', 'F')])