from mainbackend.models import Exam, Test, TestType

settings = {
    "test_type_name": "Test_type_test",
    "test_type_description": "Test_type_description"
}

t = TestType(**settings)
t.save()