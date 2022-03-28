from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import *
from django.template import loader
from .forms import *
from .audio_gen import *
from time import strftime, gmtime
from .person import *
from django.core.cache import cache
from django.contrib.auth import authenticate
import os
import random

def randomise():
    return random.choice([-1, 1])


def index(request):
    if request.session.get('person'):
        return redirect('/welcome/')
    

def acr_test(request):
    if request.method == 'POST':
        save_results(request, request.POST.get("score"))
        request.session['person']['current_test']['iteration'] += 1
        request.session.modified = True
        return redirect("Absolute Category Rating")
    file_number = request.session['person']['current_test']['iteration']
    fileset_name = request.session['person']['current_test']['parameter_1']
    scale = request.session['person']['current_test']['parameter_3']
    form = ACRTest(scale)
    fileset = Fileset.objects.get(fileset_name=fileset_name)
    if file_number > fileset.amount:
        request.session['person']['test_number'] += 1
        request.session.modified = True
        return redirect('exam_handle')
    file_destination = FileDestination.objects.get(fileset=fileset, file_number=file_number)
    return render(request, 'mainbackend/acr_test.html', {
        'form': form, 
        'destination': file_destination.file_destination,
        'test_no': request.session['person']['test_number'],
        'test_amount': request.session['person']['exam']['test_amount']
        })
    
def dcr_test(request): 
    if request.method == 'POST':
        save_results(request, request.POST.get("score"))
        request.session['person']['current_test']['iteration'] += 1
        request.session.modified = True
        return redirect("Degradation Category Rating")
    file_number = request.session['person']['current_test']['iteration']
    fileset_name = request.session['person']['current_test']['parameter_1']
    form = DCRTest()
    fileset = Fileset.objects.get(fileset_name=fileset_name)
    if file_number > fileset.amount:
        request.session['person']['test_number'] += 1
        request.session.modified = True
        return redirect('exam_handle')
    file_destination = FileDestination.objects.filter(fileset=fileset, file_number=file_number).order_by('id').all()
    return render(request, 'mainbackend/dcr_test.html', {
        'form': form, 
        'destinationA': file_destination[0].file_destination,
        'destinationB': file_destination[1].file_destination,
        'test_no': request.session['person']['test_number'],
        'test_amount': request.session['person']['exam']['test_amount'],
        'presentation': request.session['person']['current_test']['parameter_3']
        })

    
def ccr_test(request): 
    request.session['person']['current_test']['order'] = randomise()
    if request.method == 'POST':
        save_results(request, request.POST.get("score") * request.session['person']['current_test']['order'])
        request.session['person']['current_test']['iteration'] += 1
        request.session.modified = True
        return redirect("Degradation Category Rating")
    file_number = request.session['person']['current_test']['iteration']
    fileset_name = request.session['person']['current_test']['parameter_1']
    form = CCRTest()
    fileset = Fileset.objects.get(fileset_name=fileset_name)
    if file_number > fileset.amount:
        request.session['person']['test_number'] += 1
        request.session.modified = True
        return redirect('exam_handle')
    file_destination = FileDestination.objects.filter(fileset=fileset, file_number=file_number).order_by('id').all()
    return render(request, 'mainbackend/dcr_test.html', {
        'form': form, 
        'destinationA': file_destination[0].file_destination,
        'destinationB': file_destination[1].file_destination,
        'test_no': request.session['person']['test_number'],
        'test_amount': request.session['person']['exam']['test_amount'],
        'presentation': request.session['person']['current_test']['parameter_3'],
        'order': request.session['person']['current_test']['order'] 
        })


def mushra(request): 
    fileset_name = request.session['person']['current_test']['parameter_1']
    fileset = Fileset.objects.get(fileset_name=fileset_name)
    if request.method == 'POST':
        request.session['person']['current_test']['iteration'] = 1
        print(request.POST)
        for i in range(1, int(fileset.amount) + 1):
            save_results(request, request.POST.get(f'result_{i}'))
            request.session['person']['current_test']['iteration'] += 1
            request.session.modified = True
        request.session['person']['test_number'] += 1
        request.session.modified = True
        return redirect("exam_handle")
    form = MUSHRATest(int(fileset.amount))
    file_destination = FileDestination.objects.filter(fileset=fileset).order_by('file_number').all()
    return render(request, 'mainbackend/mushra.html', {
        'form': form, 
        'destination': file_destination,
        'test_no': request.session['person']['test_number'],
        'test_amount': request.session['person']['exam']['test_amount'],
        'amount': fileset.amount
        })