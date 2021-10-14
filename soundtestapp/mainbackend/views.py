from django.shortcuts import render
from django.http import HttpResponse
from .models import ExaminationResult
from django.template import loader

def index(request):
    first_person = ExaminationResult.objects.all()[0]
    template = loader.get_template('mainbackend/index.html')
    context = {
        'first_person': first_person,
    }
    return HttpResponse(template.render(context, request))