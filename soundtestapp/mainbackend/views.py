from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import ExaminationResult, ExaminedPerson, Exam, Test, TestType
from django.template import loader
from .forms import *
from .audio_gen import *
from time import strftime, gmtime
from .person import *

def index(request):
    if request.session.get('person'):
        return redirect('/welcome/')
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            create_person(request, form, ExaminedPerson)
            return redirect('/welcome/')
    return render(request, 'mainbackend/index.html', {'form': form, 'user_login': request.session.get('person')})


def welcome(request):
    if not request.session.get('person'):
        return redirect('/')
    exams = Exam.objects.filter(status="O")
    if request.method == 'POST':
        exam_id = list(filter(lambda a: 'exam:' in a, request.POST.keys()))[0]
        request.session['person']['test_no'] = 1
        return redirect('exam_handle', exam_id=exam_id[5:], test_no=1)
    name = request.session.get('person').get('first_name')
    return render(request, 'mainbackend/welcome.html', {'name': name, 'exams': exams, 'user_login': request.session.get('person')})


def interrupt(request):
    if not request.session.get('person'):
        return redirect('/')
    del_person(request, ExaminedPerson)
    return redirect('/')


def exam_handle(request, exam_id, test_no):
    if not request.session.get('person'):
        return redirect('/')
    exam = Exam.objects.filter(exam_name=exam_id)[0]
    tests = list(filter(lambda a: 'test' in a, exam.__dict__))
    if test_no > exam.test_amount:
        return redirect('end_exam') 
    test = exam.__dict__[f'test{test_no}_id_id']
    test_type = exam.__dict__[f'test{test_no}_type_id']
    request.session['person'][f'test{test_no}'] = {
        "test": test,
        "test_type": test_type,
        "delta": 5,
        "step": 0.2,
    }
    request.session.modified = True
    return redirect('make_test', exam_id=exam_id, test_id=test, test_type_id=test_type, test_no=test_no)


def make_test(request, exam_id, test_id, test_type_id, test_no):
    if not request.session.get('person'):
        return redirect('/')
        
    exam = Exam.objects.filter(exam_name=exam_id)[0]
    test = Test.objects.filter(id=test_id)[0]
    test_type = TestType.objects.filter(id=test_type_id)[0]
    dt_gmt = strftime("%Y-%m-%d_%H-%M-%S", gmtime())
    filename, choice = eval(f"{test.function}(randomise_delta(request.session['person'][f'test{test_no}']['delta']), request.session.get('person').get('first_name'), dt_gmt)")
    filename = filename.split('/')[-1]

    if request.method == "POST":
        button = list(request.POST.keys())[1]
        print(button, choice)
        if button == choice:
            request.session['person'][f'test{test_no}']['delta'] -= request.session['person'][f'test{test_no}']['step']
            request.session.modified = True
            return redirect('make_test', exam_id=exam_id, test_id=test_id, test_type_id=test_type_id, test_no=test_no)
        else:
            return redirect('end_exam')
    return render(request, 'mainbackend/make_test.html', {'filename': filename, 'exam': exam, 'test_no' : test_no, 'test': test, 'test_type': test_type, 'user_login': request.session.get('person')})


def end_exam(request):
    if not request.session.get('person'):
        return redirect('/')
    request.session['person'] = None
    return render(request, 'mainbackend/end_exam.html')