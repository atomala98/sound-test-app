from mainbackend.models import *
from datetime import datetime
from time import strftime, gmtime
import os

dt_gmt = strftime("logs\db_state\%Y-%m-%d %H-%M-%S", gmtime())
logs = open(f'{dt_gmt}_log.txt', 'w')

e = ExaminedPerson.objects.all()

logs.write('Persons\n')
for i in e:
    logs.write(str(i.__dict__) + "\n")

e = Test.objects.all()

logs.write('\nTest\n')
for i in e:
    logs.write(str(i.__dict__) + "\n")

e = TestType.objects.all()

logs.write('\nTestType\n')
for i in e:
    logs.write(str(i.__dict__) + "\n")

e = Exam.objects.all()

logs.write('\nExam\n')
for i in e:
    logs.write(str(i.__dict__) + "\n")
    
e = Results.objects.all()

logs.write('\nResults\n')
for i in e:
    logs.write(str(i.__dict__) + "\n")

e = ExaminationResult.objects.all()

logs.write('\nExaminationResult\n')
for i in e:
    logs.write(str(i.__dict__) + "\n")

e = AdminACC.objects.all()

logs.write('\nAdminACC\n')
for i in e:
    logs.write(str(i.__dict__) + "\n")

e = AdminToExam.objects.all()

logs.write('\nAdminToExam\n')
for i in e:
    logs.write(str(i.__dict__) + "\n")
    
e = Fileset.objects.all()

logs.write('\nFileset\n')
for i in e:
    logs.write(str(i.__dict__) + "\n")
    
e = MUSHRATestSets.objects.all()

logs.write('\nMUSHRATestSets\n')
for i in e:
    logs.write(str(i.__dict__) + "\n")    

logs.close()