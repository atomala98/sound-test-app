from django.shortcuts import render, redirect
from .models import ExaminationResult, AdminACC, Test, Exam, AdminToExam
from django.template import loader
from .forms import *

def login(request):
    if request.session.get('admin'):
        return redirect('admin_panel')
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
                else:
                    message = "Wrong password"
                    return render(request, 'mainbackend/admin_logon.html', {'form': form, 'messages': [message]})
            else:
                message = f"No account with login {login}"
                return render(request, 'mainbackend/admin_logon.html', {'form': form, 'messages': [message]})
    return render(request, 'mainbackend/admin_logon.html', {'form': form})


def admin_panel(request):
    if not request.session.get('admin'):
        return redirect('login')
    login = request.session['admin']['login']
    admin = AdminACC.objects.filter(login = login)[0]
    return render(request, 'mainbackend/admin_panel.html', {'admin': admin})


def create_exam(request):
    if not request.session.get('admin'):
        return redirect('login')
    login = request.session['admin']['login']
    admin = AdminACC.objects.filter(login = login)[0]
    form = CreateExam()
    if request.method == 'POST':
        form = CreateExam(request.POST)
        if form.is_valid():
            exam_name = form.cleaned_data['exam_name']
            test1_id = Test.objects.filter(id=request.POST['test1'][0])[0]
            test1_type = TestType.objects.filter(id=request.POST['test1_type'][0])[0]
            if not Exam.objects.filter(exam_name=exam_name):
                exam = Exam(exam_name=exam_name, test1_id=test1_id, test1_type=test1_type, status="O")
                exam.save()
                admin_to_exam = AdminToExam(admin_id=admin, exam_id=exam)
                admin_to_exam.save()
                return redirect('admin_panel')
            else:
                message = 'Test name already taken'
                return render(request, 'mainbackend/create_exam.html', {'admin': admin, 'form': form, 'messages': [message]})
    return render(request, 'mainbackend/create_exam.html', {'admin': admin, 'form': form})
    

def logout(request):
    request.session['admin'] = None
    return redirect('login')