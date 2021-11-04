from mainbackend.models import Exam, Test

t = Test(test_name = 'test')
e = Exam(exam_name = '', test1_id = t, status = "O")