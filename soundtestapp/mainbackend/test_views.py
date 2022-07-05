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
        'test_amount': request.session['person']['exam']['test_amount'],
        'description': request.session['person']['test_description']
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
        'presentation': request.session['person']['current_test']['parameter_3'],
        'description': request.session['person']['test_description']
        })

    
def ccr_test(request): 
    if request.method == 'POST':
        save_results(request, request.POST.get("score") * request.session['person']['current_test']['order'])
        request.session['person']['current_test']['iteration'] += 1
        request.session.modified = True
        return redirect("Comparison Category Rating")
    request.session['person']['current_test']['order'] = randomise()
    request.session.modified = True
    file_number = request.session['person']['current_test']['iteration']
    fileset_name = request.session['person']['current_test']['parameter_1']
    form = CCRTest()
    fileset = Fileset.objects.get(fileset_name=fileset_name)
    if file_number > fileset.amount:
        request.session['person']['test_number'] += 1
        request.session.modified = True
        return redirect('exam_handle')
    file_destination = FileDestination.objects.filter(fileset=fileset, file_number=file_number).order_by('id').all()
    return render(request, 'mainbackend/ccr_test.html', {
        'form': form, 
        'destinationA': file_destination[0].file_destination,
        'destinationB': file_destination[1].file_destination,
        'test_no': request.session['person']['test_number'],
        'test_amount': request.session['person']['exam']['test_amount'],
        'presentation': request.session['person']['current_test']['parameter_3'],
        'order': request.session['person']['current_test']['order'],
        'description': request.session['person']['test_description']
        })


def mushra(request): 
    fileset_name = request.session['person']['current_test']['parameter_1']
    fileset = Fileset.objects.get(fileset_name=fileset_name)
    if request.method == 'POST':
        request.session['person']['current_test']['iteration'] = 1
        for i in range(1, int(fileset.amount) + 1):
            save_results(request, request.POST.get(f'result_{i}'))
            request.session['person']['current_test']['iteration'] += 1
            request.session.modified = True
        request.session['person']['test_number'] += 1
        request.session.modified = True
        return redirect("exam_handle")
    form = MUSHRATest(int(fileset.amount))
    file_destination = FileDestination.objects.filter(fileset=fileset).order_by('file_number').all()
    original_file = file_destination[0]
    file_destination = file_destination[1:]
    return render(request, 'mainbackend/mushra.html', {
        'form': form, 
        'original': original_file,
        'destination': file_destination,
        'test_no': request.session['person']['test_number'],
        'test_amount': request.session['person']['exam']['test_amount'],
        'amount': fileset.amount,
        'description': request.session['person']['test_description']
        })
    
    
def abx_test(request): 
    if request.method == 'POST':
        save_results(request, max('0', request.POST.get("score") * request.session['person']['current_test']['order']))
        request.session['person']['current_test']['iteration'] += 1
        request.session.modified = True
        return redirect("ABX Test")
    request.session['person']['current_test']['order'] = randomise()
    request.session.modified = True
    file_number = request.session['person']['current_test']['iteration']
    fileset_name = request.session['person']['current_test']['parameter_1']
    form = ABXTest()
    fileset = Fileset.objects.get(fileset_name=fileset_name)
    if file_number > fileset.amount:
        request.session['person']['test_number'] += 1
        request.session.modified = True
        return redirect('exam_handle')
    file_destination = FileDestination.objects.filter(fileset=fileset, file_number=file_number).order_by('id').all()
    return render(request, 'mainbackend/ABX_test.html', {
        'form': form, 
        'destinationA': file_destination[0].file_destination,
        'destinationB': file_destination[1].file_destination,
        'test_no': request.session['person']['test_number'],
        'test_amount': request.session['person']['exam']['test_amount'],
        'order': request.session['person']['current_test']['order'],
        'description': request.session['person']['test_description'] 
        })
    
    
def abchr_test(request): 
    if request.method == 'POST':
        if request.session['person']['current_test']['order'] == 1:
            save_results(request, request.POST.get("first_score"))
        if request.session['person']['current_test']['order'] == -1:
            save_results(request, request.POST.get("second_score"))
        request.session['person']['current_test']['iteration'] += 1
        request.session.modified = True
        return redirect("ABC/HR Test")
    request.session['person']['current_test']['order'] = randomise()
    request.session.modified = True
    file_number = request.session['person']['current_test']['iteration']
    fileset_name = request.session['person']['current_test']['parameter_1']
    form = ABCHRTest()
    fileset = Fileset.objects.get(fileset_name=fileset_name)
    if file_number > fileset.amount:
        request.session['person']['test_number'] += 1
        request.session.modified = True
        return redirect('exam_handle')
    file_destination = FileDestination.objects.filter(fileset=fileset, file_number=file_number).order_by('id').all()
    return render(request, 'mainbackend/ABCHR_test.html', {
        'form': form, 
        'destinationA': file_destination[0].file_destination,
        'destinationB': file_destination[1].file_destination,
        'test_no': request.session['person']['test_number'],
        'test_amount': request.session['person']['exam']['test_amount'],
        'order': request.session['person']['current_test']['order'],
        'description': request.session['person']['test_description']
        })
    
    