from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import ExaminationResult, ExaminedPerson, Exam, Test, TestType, Result, ExamTest
from django.template import loader
from .forms import *
from .audio_gen import *
from time import strftime, gmtime
from .person import *
from django.core.cache import cache
from django.contrib.auth import authenticate
import os

def index(request):
    if request.session.get('person'):
        return redirect('/welcome/')
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            create_person(request, form)
            return redirect('/welcome/')
    return render(request, 'mainbackend/index.html', {'form': form, 'user_login': request.session.get('person')})


def welcome(request):
    if not request.session.get('person'):
        return redirect('/')
    exams = Exam.objects.filter(status="O")
    if request.method == 'POST':
        exam_id = list(filter(lambda a: 'exam:' in a, request.POST.keys()))[0][5:]
        exam = Exam.objects.get(exam_name=exam_id)
        request.session['person']['exam_id'] = exam_id
        request.session.modified = True
        return redirect('exam_handle', exam_id=exam.id, test_no=1)
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
    exam = Exam.objects.get(id=exam_id)
    if test_no > exam.test_amount:
        return redirect('end_exam')
    print(exam, test_no)
    test = ExamTest.objects.get(exam=exam, test_number=test_no)
    return redirect('make_test', exam=exam.id, exam_test=test.id, test_no=test_no)

def make_test(request, exam, exam_test, test_no):
    if not request.session.get('person'):
        return redirect('/')
        
    exam = Exam.objects.filter(id=exam)[0]
    test = ExamTest.objects.filter(id=exam_test)[0]
    
    dt_gmt = strftime("%Y-%m-%d_%H-%M-%S", gmtime())
    if request.method == "GET":
        filename_path, temp = eval(f"{test.test.function}(randomise_delta(5), request.session.get('person').get('first_name'), dt_gmt)")
        request.session.modified = True
        filename = filename_path.split('/')[-1]

    if request.method == "POST":
        # button = list(request.POST.keys())[1]
        # print(button, request.session['person'][f'test{test_no}']['choice'])
        # if button == request.session['person'][f'test{test_no}']['choice']:
        #     request.session['person'][f'test{test_no}']['delta'] -= request.session['person'][f'test{test_no}']['step']
        #     request.session.modified = True
        #     print(filename)
        #     return redirect('make_test', exam=exam.id, exam_test=test.id, test_no=test_no)
        # else:
        return redirect('exam_handle', exam_id=exam.id, test_no=test_no + 1)
    return render(request, 'mainbackend/frequency_difference.html', {'filename': filename, 'exam': exam, 'test_no' : test_no, 'test': test, 'user_login': request.session.get('person')})


def end_exam(request):
    if not request.session.get('person'):
        return redirect('/')
    save_results(request)
    request.session['person'] = None
    return render(request, 'mainbackend/end_exam.html')