from django.db.models import Q

def create_person(request, form, ExaminedPerson):
    request.session['person'] = {}
    request.session['person']['first_name'] = form.cleaned_data['first_name']
    request.session['person']['last_name'] = form.cleaned_data['last_name']
    person = ExaminedPerson(**form.cleaned_data)
    person.save()
    request.session['person']['id'] = person.id


def del_person(request, ExaminedPerson):
    id = request.session.get('person').get('id')
    person = ExaminedPerson.objects.filter(id=id)[0]
    person.delete()
    request.session['person'] = None


def save_results(request, ExaminedPerson, Exam, ExaminationResult):
    person_id = request.session.get('person').get('id')
    results = {
        "person_id": ExaminedPerson.objects.filter(id=person_id)[0],
    }
    exam_result = ExaminationResult(**results)
    exam_result.save()