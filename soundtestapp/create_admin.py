from mainbackend.models import AdminACC

credintials = {
    'login': "Admin",
    'password': "1234",
    'first_name': "Admin",
    'last_name': "Account",
}

adminacc = AdminACC(**credintials)
adminacc.save()