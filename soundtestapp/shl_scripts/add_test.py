from mainbackend.models import Exam, Test, TestType

settings = {
    "name": "Frequency difference test",
    "description": "This is frequency difference test"
}

t = Test(**settings)
t.save()