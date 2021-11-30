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


def save_results(request, ExaminedPerson, Exam, ExaminationResult, Results):
    person_id = request.session.get('person').get('id')
    exam_id = request.session.get('person').get('exam_id')
    exam_results = {
        "person_id": ExaminedPerson.objects.filter(id=person_id)[0],
        "exam_id": Exam.objects.filter(exam_name=exam_id)[0],
    }
    result_dict = {}
    for i in range(exam_results["exam_id"].test_amount):
        result_dict[f'test{i + 1}_result'] = request.session['person'][f'test{i + 1}']['delta']
    results = Results(**result_dict)
    results.save()
    exam_results['results_id'] = results
    exam_result = ExaminationResult(**exam_results)
    exam_result.save()