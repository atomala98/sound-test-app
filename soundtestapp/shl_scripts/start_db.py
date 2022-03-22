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
    "function": "ACR_test",
}

t = Test(**settings)
t.save()


settings = {
    "name": "Degradation Category Rating",
    "description": "This is Degradation Category Rating test",
    "function": "DCR_test",
}

t = Test(**settings)
t.save()


settings = {
    "name": "Comparison Category Rating",
    "description": "This is Comparison Category Rating test",
    "function": "CCR_test",
}

t = Test(**settings)
t.save()