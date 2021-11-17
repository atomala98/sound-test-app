from mainbackend.models import Exam, Test, TestType

settings = {
    "name": "Method of Limits",
    "description": "Method of limits is method"
}

t = TestType(**settings)
t.save()