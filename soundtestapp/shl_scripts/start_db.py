from mainbackend.models import *
from django.contrib.auth.hashers import make_password

credintials = {
    'login': "Admin2",
    'password': make_password("1234"),
    'first_name': "Admin",
    'last_name': "Account",
}

adminacc = AdminACC(**credintials)
adminacc.save()

settings = {
    "name": "Frequency difference test",
    "description": "This is frequency difference test",
    "function": "frequency_difference_test",
}

t = Test(**settings)
t.save()



settings = {
    "name": "Absolute Category Rating",
    "description": "This is Absolute Category Rating test",
    "function": "ACT_test",
}

t = Test(**settings)
t.save()