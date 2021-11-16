from mainbackend.models import Exam, Test, TestType

t = Test(test_name = 'test', test_description = 'asdzxc')
c = TestType(test_type_name = 'type', test_type_description = 'desc')
e = Exam(exam_name = 'exam', test1_id = t, test1_type = c, status = "O")