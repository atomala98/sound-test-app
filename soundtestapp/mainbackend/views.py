from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import ExaminationResult, ExaminedPerson, Exam, Test, TestType
from django.template import loader
from django.db.models import Q
from .forms import *

def index(request):
    if request.session.get('person'):
        return redirect('/welcome/')
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            request.session['person'] = {}
            request.session['person']['first_name'] = form.cleaned_data['first_name']
            request.session['person']['last_name'] = form.cleaned_data['last_name']
            person = ExaminedPerson(**form.cleaned_data)
            person.save()
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
    first_name = request.session.get('person').get('first_name')
    last_name = request.session.get('person').get('last_name')
    person = ExaminedPerson.objects.filter(Q(first_name = first_name) | Q(last_name = last_name))
    person.delete()
    request.session['person'] = None
    return redirect('/')

def exam_handle(request, exam_id, test_no):
    exam = Exam.objects.filter(exam_name=exam_id)[0]
    tests = list(filter(lambda a: 'test' in a, exam.__dict__))
    test = exam.__dict__[f'test{test_no}_id_id']
    test_type = exam.__dict__[f'test{test_no}_type_id']
    return redirect('make_test', exam_id=exam_id, test_id=test, test_type_id=test_type, test_no=test_no)

def make_test(request, exam_id, test_id, test_type_id, test_no):
    test = Test.objects.filter(id=test_id)
    test_type = TestType.objects.filter(id=test_type_id)
    return render(request, 'mainbackend/make_test.html', {'test': test, 'user_login': request.session.get('person')})