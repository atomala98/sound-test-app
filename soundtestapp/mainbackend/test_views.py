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
    
    
