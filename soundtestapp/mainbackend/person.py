from django.db.models import Q
from .models import ExaminedPerson, ExamTest, ExaminationResult, Result
import datetime

def create_person(request, form):
    request.session['person'] = {}
    request.session['person']['first_name'] = form.cleaned_data['first_name']
    request.session['person']['last_name'] = form.cleaned_data['last_name']
    person = ExaminedPerson(**form.cleaned_data)
    person.save()
    request.session['person']['id'] = person.id
    
    
def start_exam(request, person, exam):
    exam_result = ExaminationResult(
        person_id=person,
        exam_id=exam,
        start_date=datetime.datetime.now(),
        exam_finished="F"
    )
    exam_result.save()
    request.session['person']['result_id'] = exam_result.id


def del_person(request, ExaminedPerson):
    id = request.session.get('person').get('id')
    person = ExaminedPerson.objects.filter(id=id).first()
    if person:
        person.delete()
    request.session['person'] = None


def save_results(request, test_result):
    exam_result_id = request.session['person']['result_id']
    exam_result = ExaminationResult.objects.get(id=exam_result_id)
    test_id = request.session['person']['current_test']['test_id']
    test = ExamTest.objects.get(id=test_id)
    existing_result = Result.objects.filter(examination_result=exam_result,
            exam_test=test,
            result_number=request.session['person']['current_test']['iteration'])
    if not existing_result:
        result = Result(
            examination_result=exam_result,
            exam_test=test,
            result=test_result,
            result_number=request.session['person']['current_test']['iteration']
        )
        result.save()
    else:
        if existing_result[0].result == '':
            existing_result[0].result = result
            existing_result[0].save() 
    

def end_exam_function(request):
    exam_result_id = request.session['person']['result_id']
    exam_result = ExaminationResult.objects.get(id=exam_result_id)
    exam_result.end_date = datetime.datetime.now()
    exam_result.exam_finished = "T"
    exam_result.save()
    request.session['person'] = None
    request.session.modified = True