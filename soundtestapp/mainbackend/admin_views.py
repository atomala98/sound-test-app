from django.shortcuts import render, redirect
from .models import ExaminationResult, AdminACC
from django.template import loader
from .forms import *

def login(request):
    print(request.session.__dict__)
    form = AdminLoginForm()
    if request.method == 'POST':
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            login = form.cleaned_data['login']
            admin = AdminACC.objects.filter(login = login)
            if admin:
                admin = admin[0]
                password = form.cleaned_data['password']
                if admin.password == password: 
                    request.session['admin'] = {}
                    request.session['admin']['login'] = login
                    return redirect('admin_panel')
    return render(request, 'mainbackend/admin_logon.html', {'form': form})


def admin_panel(request):
    print(request.session.__dict__)
    login = request.session['admin']['login']
    admin = AdminACC.objects.filter(login = login)[0]
    first_name = admin.first_name
    last_name = admin.last_name
    return render(request, 'mainbackend/admin_panel.html', {'first_name': first_name, 'last_name': last_name})


def logout(request):
    request.session['admin'] = None
    return redirect('login')