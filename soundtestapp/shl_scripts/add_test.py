from mainbackend.models import Exam, Test, TestType

settings = {
    "test_name": "Test_test",
    "test_description": "Test_description"
}

t = Test(**settings)
t.save()