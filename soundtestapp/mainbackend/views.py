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
    if request.session['person'].get('test_number'):
        return redirect('exam_handle')
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
    request.session['person']['test_description'] = test.test.description
    request.session['person']['current_test'] = test.toJSON()
    request.session.modified = True
    return redirect(test.redirect())


def end_exam(request):
    if not request.session.get('person'):
        return redirect('/')
    return render(request, 'mainbackend/end_exam.html')