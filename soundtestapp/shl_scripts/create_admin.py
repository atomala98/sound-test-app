from mainbackend.models import AdminACC
from django.contrib.auth.hashers import make_password

credintials = {
    'login': "Admin2",
    'password': make_password("1234"),
    'first_name': "Admin",
    'last_name': "Account",
}

adminacc = AdminACC(**credintials)
adminacc.save()