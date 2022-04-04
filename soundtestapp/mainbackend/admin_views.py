from django.shortcuts import render, redirect
from .models import *
from django.template import loader
from .forms import *
from django.contrib.auth.hashers import check_password
from operator import add
import os

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
    test_amount = 2
    admin = AdminACC.objects.filter(login = login)[0]
    form = CreateExam(test_amount)
    if request.method == 'POST':
        form = CreateExam(test_amount, request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            exam_name = form_data['exam_name']
            if not Exam.objects.filter(exam_name=exam_name):
                exam = Exam(exam_name=exam_name, test_amount=test_amount, status="W")
                exam.save()
                for i in range(1, test_amount + 1):
                    test = ExamTest(test_number=i, exam=exam, test=form_data[f'test_{i}'])
                    test.save()
                admin_to_exam = AdminToExam(admin=admin, exam=exam)
                admin_to_exam.save()
                return redirect('add_parameters', exam_id=exam.id)
            else:
                message = 'Test name already taken'
                return render(request, 'mainbackend/create_exam.html', {'admin': admin, 'form': form, 'messages': [message]})
    return render(request, 'mainbackend/create_exam.html', {'admin': admin, 'form': form})
    
    
def add_parameters(request, exam_id):
    forms_dict = {
        "Frequency difference test": FrequencyDifferenceParameters,
        "Absolute Category Rating": ACRParameters,
        "Degradation Category Rating": DCRParameters,
        "Comparison Category Rating": CCRParameters,
        "MUSHRA": MUSHRAParameters,
        "ABX Test": ABXParameters
    }
    if not request.session.get('admin'):
        return redirect('login')
    exam = Exam.objects.get(id=exam_id)
    exam_tests = ExamTest.objects.filter(exam=exam)
    parameter_forms = []
    if request.method == 'POST':
        for i, test in enumerate(exam_tests):
            form = forms_dict[test.test.name](i + 1, request.POST)
            if form.is_valid():
                parameter_forms.append(form.cleaned_data)
            else:
                return redirect('add_parameters', exam_id=exam_id)
        for i, parameters in enumerate(parameter_forms):
            for j, (_, parameter) in enumerate(parameters.items()):
                exam_tests[i].__dict__[f'parameter_{j+1}'] = str(parameter)
            exam_tests[i].save()
        exam.status = "O"
        exam.save()
        return redirect('admin_panel')
    for i, test in enumerate(exam_tests):
        parameter_forms.append({
            'name': test.test.name,
            'form': forms_dict[test.test.name](i + 1), 
        })
    print(parameter_forms)
    return render(request, 'mainbackend/add_parameters.html', {"parameter_forms": parameter_forms})
        
    
def exam_list(request):
    if not request.session.get('admin'):
        return redirect('login')
    login = request.session['admin']['login']
    admin = AdminACC.objects.get(login = login)
    exams = map(lambda a: a.exam, AdminToExam.objects.filter(admin=admin))
    if request.method == 'POST':
        print(request.POST)
    return render(request, 'mainbackend/exam_list.html', {'exams': exams})


def open_exam(request, exam_id):
    if not request.session.get('admin'):
        return redirect('login')
    exam = Exam.objects.get(id=exam_id)
    exam.status = "O"
    exam.save()
    return redirect('exam_list')


def delete_exam(request, exam_id):
    if not request.session.get('admin'):
        return redirect('login')
    exam = Exam.objects.get(id=exam_id).delete()
    return redirect('exam_list')


def close_exam(request, exam_id):
    if not request.session.get('admin'):
        return redirect('login')
    exam = Exam.objects.get(id=exam_id)
    exam.status = "C"
    exam.save()
    return redirect('exam_list')


def check_exam(request, exam_id):
    if not request.session.get('admin'):
        return redirect('login')
    exam = Exam.objects.get(id=exam_id)
    exam_tests = ExamTest.objects.filter(exam=exam).all().order_by('test_number')
    tests = []
    files = []
    for test in exam_tests:
        fileset = Fileset.objects.get(fileset_name=test.parameter_1)
        tests.append({
            'name': f"{test.test.name} - Fileset: {fileset.fileset_name}",
            'length': int(fileset.amount)
        })
        files += FileDestination.objects.filter(fileset=fileset).values_list('file_label', flat=True)
    exam_results = ExaminationResult.objects.filter(exam_id=exam).all().order_by('-start_date')
    results = []
    means = [0]*len(files)
    finished_exams = 0
    for result in exam_results:
        results.append({
            'name': str(result.person_id),
            'start': result.start_date.strftime("%m/%d/%Y, %H:%M:%S"),
            'results': list(map(lambda a: int(a.result), Result.objects.filter(examination_result=result, result__isnull=False).all()))
        })
        if len(results[-1]['results']):
            means = list(map(add, means, results[-1]['results']))
            finished_exams += 1
    means = list(map(lambda a: a / finished_exams, means))
    return render(request, 'mainbackend/check_exam.html', {
        'results': results,
        'files': files,
        'exam_tests': tests,
        'tests_amount': len(exam_tests),
        'means': means,
        'finished_exams': finished_exams
        })


def add_files(request):
    fileset_types_list = {
        "One": "add_one_file",
        "Two": "add_two_files",
        "MUSHRA": "add_files_MUSHRA"
    }
    
    if request.method == 'POST':
        form = AddFilesForm(request.POST)
        if form.is_valid():
            fileset_name = form.cleaned_data["fileset_name"]
            fileset_type = form.cleaned_data["fileset_type"]
            amount = form.cleaned_data["amount"]
            if Fileset.objects.filter(fileset_name=fileset_name):
                return redirect('add_files', {"message": "Fileset already exists!"})
            return redirect(fileset_types_list[fileset_type], fileset_name = fileset_name, amount = amount)
    else:
        form = AddFilesForm()
    return render(request, 'mainbackend/add_files.html', {'form': form})


def add_one_file(request, fileset_name: str, amount: int):
    if request.method == 'POST':
        form = OneFileUploadForm(amount, request.POST, request.FILES)
        if form.is_valid():
            fileset = Fileset(fileset_name=fileset_name, fileset_type="One File Set", amount=amount)
            fileset.save()
            for i in range(1, amount + 1):
                file = form.cleaned_data[f"file{i}"]
                file_label = form.cleaned_data[f"file_label{i}"]
                file.name = file.name.replace(" ", "_")
                os.mkdir(f"mainbackend/static/mainbackend/one_file/{fileset_name}")
                dest = f"mainbackend/static/mainbackend/one_file/{fileset_name}/{file.name}"
                with open(dest, 'wb+') as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)
                file_db = FileDestination(
                    fileset=fileset, 
                    filename=file.name, 
                    file_label=file_label,
                    file_destination=f"mainbackend/one_file/{fileset_name}/{file.name}",
                    file_number=i
                    )   
                file_db.save()   
            return redirect('admin_panel')     
    else:
        form = OneFileUploadForm(amount)
    return render(request, 'mainbackend/add_files_template.html', {'form': form})


def add_two_files(request, fileset_name: str, amount: int):
    if request.method == 'POST':
        form = TwoFilesUploadForm(amount, request.POST, request.FILES)
        if form.is_valid():
            fileset = Fileset(fileset_name=fileset_name, fileset_type="Two File Set", amount=amount)
            fileset.save()
            for i in range(1, amount + 1):
                file = form.cleaned_data[f"file_A{i}"]
                file_label = form.cleaned_data[f"file_label_A{i}"]
                file.name = file.name.replace(" ", "_")
                os.mkdir(f"mainbackend/static/mainbackend/two_files/{fileset_name}")
                dest = f"mainbackend/static/mainbackend/two_files/{fileset_name}/{file.name}"
                with open(dest, 'wb+') as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)
                file_A_db = FileDestination(
                    fileset=fileset, 
                    filename=file.name, 
                    file_label=file_label,
                    file_destination=f"mainbackend/two_files/{fileset_name}/{file.name}",
                    file_number=i
                    )   
                file_A_db.save()   
                file = form.cleaned_data[f"file_B{i}"]
                file_label = form.cleaned_data[f"file_label_B{i}"]
                file.name = file.name.replace(" ", "_")
                dest = f"mainbackend/static/mainbackend/two_files/{fileset_name}/{file.name}"
                with open(dest, 'wb+') as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)
                file_B_db = FileDestination(
                    fileset=fileset, 
                    filename=file.name, 
                    file_label=file_label,
                    file_destination=f"mainbackend/two_files/{fileset_name}/{file.name}",
                    file_number=i
                    )   
                file_B_db.save()   
            return redirect('admin_panel')     
    else:
        form = TwoFilesUploadForm(amount)
    return render(request, 'mainbackend/add_files_template.html', {'form': form})


def add_files_MUSHRA(request, fileset_name: str, amount: int) -> render:
    if request.method == 'POST':
        form = MUSHRATestUpload(amount, request.POST, request.FILES)
        if form.is_valid():
            fileset = Fileset(fileset_name=fileset_name, fileset_type="MUSHRA Set", amount=amount)
            fileset.save()
            for i in range(1, amount + 1):
                file = form.cleaned_data[f"file{i}"]
                file_label = form.cleaned_data[f"file_label{i}"]
                file.name = file.name.replace(" ", "_")
                os.mkdir(f"mainbackend/static/mainbackend/mushra/{fileset_name}")
                dest = f"mainbackend/static/mainbackend/mushra/{fileset_name}/{file.name}"
                with open(dest, 'wb+') as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)
                file_db = FileDestination(
                    fileset=fileset, 
                    filename=file.name, 
                    file_label=file_label,
                    file_destination=f"mainbackend/mushra/{fileset_name}/{file.name}",
                    file_number=i
                    )   
                file_db.save()   
            return redirect('admin_panel')     
    else:
        form = MUSHRATestUpload(amount)
    return render(request, 'mainbackend/add_files_mushra.html', {'form': form})


def logout(request):
    request.session['admin'] = None
    return redirect('login')