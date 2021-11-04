from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import ExaminationResult, ExaminedPerson,Exam
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
        return redirect('/welcome/')
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