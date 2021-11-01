from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import ExaminationResult, ExaminedPerson,Exam
from django.template import loader
from django.db.models import Q
from .forms import *

def index(request):
    # if request.session.get('person'):
    #     return redirect('/welcome/')
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            request.session['first_name'] = form.cleaned_data['first_name']
            request.session['last_name'] = form.cleaned_data['last_name']
            person = ExaminedPerson(**form.cleaned_data)
            person.save()
            print(person.start_date)
            return redirect('/welcome/')
    else:
        form = RegisterForm()
    return render(request, 'mainbackend/index.html', {'form': form})


def welcome(request):
    exams = Exam.objects.filter(status="O")
    if request.session.get('first_name'):
        name = request.session.get('first_name')
        return render(request, 'mainbackend/welcome.html', {'name': name, 'exams': exams})
    else:
        return redirect('/')


def interrupt(request):
    first_name = request.session.get('first_name')
    last_name = request.session.get('last_name')
    person = ExaminedPerson.objects.filter(Q(first_name = first_name) | Q(last_name = last_name))
    print(person)
    person.delete()
    request.session.person = None
    return redirect('/')