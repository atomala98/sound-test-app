from mainbackend.models import AdminACC
from django.contrib.auth.hashers import make_password

credintials = {
    'login': "atomala",
    'password': make_password("atatat"),
    'first_name': "Andrzej",
    'last_name': "Tomala",
}

adminacc = AdminACC(**credintials)
adminacc.save()