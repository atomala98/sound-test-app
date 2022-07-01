from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import *
from django.template import loader
from .forms import *
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
        exam_name = list(filter(lambda a: 'exam:' in a, request.POST.keys()))[0][5:]
        exam = Exam.objects.get(exam_name=exam_name)
        person_id = request.session.get('person').get('id')
        person = ExaminedPerson.objects.get(id=person_id)
        request.session['person']['exam'] = exam.toJSON()
        request.session['person']['test_number'] = 1
        request.session.modified = True
        start_exam(request, person, exam)
        return redirect('exam_handle')
    name = request.session.get('person').get('first_name')
    return render(request, 'mainbackend/welcome.html', {'name': name, 'exams': exams, 'user_login': request.session.get('person')})


def interrupt(request):
    if not request.session.get('person'):
        return redirect('/')
    del_person(request, ExaminedPerson)
    return redirect('/')


def exam_handle(request):
    exam_id = request.session['person']['exam']['exam_id']
    test_number = request.session['person']['test_number']
    if not request.session.get('person'):
        return redirect('/')
    exam = Exam.objects.get(id=exam_id)
    if test_number > exam.test_amount:
        end_exam_function(request)
        return redirect('end_exam')
    test = ExamTest.objects.get(exam=exam, test_number=test_number)
    request.session['person']['test_description'] = Test.objects.get(id=test.test_id).description
    request.session['person']['current_test'] = test.toJSON()
    request.session.modified = True
    return redirect(test.redirect())


def make_test(request):
    exam_id = request.session['person']['exam_id']
    test_id = request.session['person']['test_id']
    test_number = request.session['person']['test_number']
    
    if not request.session.get('person'):
        return redirect('/')
        
    exam = Exam.objects.filter(id=exam_id)[0]
    test = ExamTest.objects.filter(id=test_id)[0]
    
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
        request.session['person']['test_number'] += 1
        request.session.modified = True
        save_results(request, 5)
        return redirect('exam_handle')
    return render(request, 'mainbackend/frequency_difference.html', {'filename': filename, 'exam': exam, 'test_no' : test_number, 'test': test, 'user_login': request.session.get('person')})


def end_exam(request):
    if not request.session.get('person'):
        return redirect('/')
    return render(request, 'mainbackend/end_exam.html')