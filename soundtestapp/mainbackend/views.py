from django.shortcuts import render
from django.shortcuts import render
from .models import ExaminationResult
from django.template import loader
from .forms import *

def index(request):
    form = RegisterForm()
    return render(request, 'mainbackend/index.html', {'form': form})