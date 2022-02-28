from mainbackend.models import *

ExaminedPerson.objects.all().delete()
Test.objects.all().delete()
TestType.objects.all().delete()
Exam.objects.all().delete()
Results.objects.all().delete()
ExaminationResult.objects.all().delete()
AdminACC.objects.all().delete()
AdminToExam.objects.all().delete()
Fileset.objects.all().delete()
MUSHRATestSets.objects.all().delete()