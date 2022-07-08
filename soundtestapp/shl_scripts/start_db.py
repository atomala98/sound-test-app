from mainbackend.models import *
from django.contrib.auth.hashers import make_password

credintials = {
    'login': "atomala",
    'password': make_password("atatat12"),
    'first_name': "Andrzej",
    'last_name': "Tomala",
}

adminacc = AdminACC(**credintials)
adminacc.save()


settings = {
    "name": "Absolute Category Rating",
    "description": """
        This is Absolute Category Rating test. Click play button, to start the recording.
        Listen to the recording carefuly, and rate the recording in 1-5 scale. You can only listen to recording one.
        """,
    "function": "ACR_test",
}

t = Test(**settings)
t.save()


settings = {
    "name": "Degradation Category Rating",
    "description": """
        This is Degradation Category Rating test. Click play button, to start the recordings.
        When recordings ends, please, rate degradation level of second file in 1-5 scale.
        You can only play recordings once.
        """,
    "function": "DCR_test",
}

t = Test(**settings)
t.save()


settings = {
    "name": "Comparison Category Rating",
    "description": """
        This is Comparison Category Rating test. Click play button, to start the recordings.
        When recordings ends, please, compare audio quality of files in -3 to 3 scale.
        You can only play recordings once.
        """,
    "function": "CCR_test",
}

t = Test(**settings)
t.save()


settings = {
    "name": "MUSHRA",
    "description": """
        This is MUSHRA test. First recording is a reference one. After listening to it,
        start listening to other recordings. Rate every recording in 1-100 scale.
        You can play recordings repeatedly.
        """,
    "function": "MUSHRA",
}

t = Test(**settings)
t.save()


settings = {
    "name": "ABX Test",
    "description": """
        This is ABX test. You will hear three audio samples. First recording is a reference one,
        second one is compressed one, and third one is randomly chosen repetition of first or second
        recording. Decide if third recording is repetition of first or second recording.
        """,
    "function": "ABX_test",
}

t = Test(**settings)
t.save()

settings = {
    "name": "ABC/HR Test",
    "description": """
        This is ABC test with Hidden Reference. First recording is reference one.
        Second and third recordings are compressed recording and hidden reference.
        You have to rate quality of both recordings compared to first one in a 1-5 scale.
        """,
    "function": "ABCHR_test",
}

t = Test(**settings)
t.save()