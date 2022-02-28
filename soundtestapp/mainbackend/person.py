from django.db.models import Q
from .models import ExaminedPerson, Exam, ExaminationResult, Result

def create_person(request, form):
    request.session['person'] = {}
    request.session['person']['first_name'] = form.cleaned_data['first_name']
    request.session['person']['last_name'] = form.cleaned_data['last_name']
    person = ExaminedPerson(**form.cleaned_data)
    person.save()
    request.session['person']['id'] = person.id
    
    
def start_exam(request):
    exam_result = ExaminationResult(
        {
            'person_id': person_id,
            'exam_id': exam_id,
        }
    )
    exam_result.save()
    

def del_person(request, ExaminedPerson):
    id = request.session.get('person').get('id')
    person = ExaminedPerson.objects.filter(id=id)[0]
    person.delete()
    request.session['person'] = None


def save_results(request, person_id, exam_id):
    exam_result = ExaminationResult(
        {
            'person_id': person_id,
            'exam_id': exam_id,
        }
    )
    exam_result.save()
    results = Result({
        
    })
    results.save()
    