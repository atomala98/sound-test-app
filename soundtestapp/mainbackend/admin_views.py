from django.shortcuts import render, redirect
from .models import ExaminationResult, AdminACC, Test, Exam, AdminToExam, MUSHRATestSets, Fileset, ExamTest
from django.template import loader
from .forms import *
from django.contrib.auth.hashers import check_password

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
                if check_password(password, admin.password): 
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
            form_data = form.cleaned_data
            exam_name = form_data['exam_name']
            test_amount = 1
            if not Exam.objects.filter(exam_name=exam_name):
                exam = Exam(exam_name=exam_name, test_amount=test_amount, status="O")
                exam.save()
                test_1 = ExamTest(test_number=1, exam=exam, test=form_data['test1'])
                test_1.save()
                admin_to_exam = AdminToExam(admin_id=admin, exam_id=exam)
                admin_to_exam.save()
                return redirect('admin_panel')
            else:
                message = 'Test name already taken'
                return render(request, 'mainbackend/create_exam.html', {'admin': admin, 'form': form, 'messages': [message]})
    return render(request, 'mainbackend/create_exam.html', {'admin': admin, 'form': form})
    
    
def add_files(request):
    fileset_types_list = {
        "MUSHRA": "add_files_MUSHRA"
    }
    
    if request.method == 'POST':
        form = AddFilesForm(request.POST)
        if form.is_valid():
            fileset_name = form.cleaned_data["fileset_name"]
            fileset_type = form.cleaned_data["fileset_type"]
            if Fileset.objects.filter(fileset_name=fileset_name):
                return redirect('add_files')
            return redirect(fileset_types_list[fileset_type], fileset_name = fileset_name)
    else:
        form = AddFilesForm()
    return render(request, 'mainbackend/add_files.html', {'form': form})


def add_files_MUSHRA(request, fileset_name: str) -> render:
    if request.method == 'POST':
        form = MUSHRATestUpload(request.POST, request.FILES)
        if form.is_valid():
            original_file = form.cleaned_data["original_file"]
            original_file_label = form.cleaned_data["original_file_label"]
            filename = f"mainbackend/static/mainbackend/MUSHRA/{original_file.name}"
            with open(filename, 'wb+') as destination:
                for chunk in original_file.chunks():
                    destination.write(chunk)
            fileset = Fileset(fileset_name=fileset_name, fileset_type="MUSHRA")
            fileset.save()
            original_file_db = MUSHRATestSets(fileset=fileset, original_file_name=original_file.name, original_file_label=original_file_label)   
            original_file_db.save()   
            return redirect('admin_panel')      
    else:
        form = MUSHRATestUpload()
    return render(request, 'mainbackend/add_files_MUSHRA.html', {'form': form})


def logout(request):
    request.session['admin'] = None
    return redirect('login')