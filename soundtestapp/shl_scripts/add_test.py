from mainbackend.models import Exam, Test

settings = {
    "name": "Frequency difference test",
    "description": "This is frequency difference test",
    "function": "frequency_difference_test",
}

t = Test(**settings)
t.save()

