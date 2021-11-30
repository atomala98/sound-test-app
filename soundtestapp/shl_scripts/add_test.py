from mainbackend.models import Exam, Test, TestType

settings = {
    "name": "Frequency difference test",
    "description": "This is frequency difference test",
    "function": "frequency_difference_test",
    "first_btn": "First one",
    "second_btn": "Second one",
}

t = Test(**settings)
t.save()