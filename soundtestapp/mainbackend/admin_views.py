from django.shortcuts import render
from django.shortcuts import render
from .models import ExaminationResult
from django.template import loader
from .forms import *

def login(request):
    form = AdminLogonForm()
    return render(request, 'mainbackend/admin_logon.html', {'form': form})