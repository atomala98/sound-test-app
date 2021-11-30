from django.db.models import Q

def create_person(request, form, ExaminedPerson):
    request.session['person'] = {}
    request.session['person']['first_name'] = form.cleaned_data['first_name']
    request.session['person']['last_name'] = form.cleaned_data['last_name']
    person = ExaminedPerson(**form.cleaned_data)
    person.save()


def del_person(request, ExaminedPerson):
    first_name = request.session.get('person').get('first_name')
    last_name = request.session.get('person').get('last_name')
    person = ExaminedPerson.objects.filter(Q(first_name = first_name) & Q(last_name = last_name)).order_by('-id')[0]
    person.delete()
    request.session['person'] = None