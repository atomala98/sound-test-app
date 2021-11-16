from mainbackend.models import *
from datetime import datetime
from time import strftime, gmtime
import os

dt_gmt = strftime("logs\db_state\%Y-%m-%d %H-%M-%S", gmtime())
logs = open(f'{dt_gmt}_log.txt', 'w')

e = ExaminedPerson.objects.all()

logs.write('Persons\n')
for i in e:
    logs.write(str(i.__dict__))

e = Test.objects.all()

logs.write('\nTest\n')
for i in e:
    logs.write(str(i.__dict__))

e = TestType.objects.all()

logs.write('\nTestType\n')
for i in e:
    logs.write(str(i.__dict__))

e = Exam.objects.all()

logs.write('\nExam\n')
for i in e:
    logs.write(str(i.__dict__))
    
e = Results.objects.all()

logs.write('\nResults\n')
for i in e:
    logs.write(str(i.__dict__))

e = ExaminationResult.objects.all()

logs.write('\nExaminationResult\n')
for i in e:
    logs.write(str(i.__dict__))

e = AdminACC.objects.all()

logs.write('\nAdminACC\n')
for i in e:
    logs.write(str(i.__dict__))

e = AdminToExam.objects.all()

logs.write('\nAdminToExam\n')
for i in e:
    logs.write(str(i.__dict__))
