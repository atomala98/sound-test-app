from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.hashers import check_password

class ExaminedPerson(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    birth_date = models.DateTimeField('Birth date')
    GENDERS = (
        ('M', 'Male'),
        ('F', 'Female')
    )
    gender = models.CharField(max_length=1, choices=GENDERS)

    def __str__(self):
        return str(self.first_name) + " " + str(self.last_name) + "."


class Test(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, null=True)
    function = models.CharField(max_length=1000, null=True)
    first_btn = models.CharField(max_length=30, null=True)
    second_btn = models.CharField(max_length=30, null=True)

    def __str__(self):
        return str(self.name)


class TestType(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, null=True)
    question = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return str(self.name)


class Exam(models.Model):
    exam_name = models.CharField(max_length=30, null=True)
    test1_id = models.ForeignKey(Test, on_delete=models.CASCADE, null=True)
    test1_type = models.ForeignKey(TestType, on_delete=models.CASCADE, null=True)
    test_amount = models.IntegerField(null=True)
    STATUS_TYPES = (
        ('O', 'Open'),
        ('C', 'Close')
    )
    status = models.CharField(max_length=1, choices=STATUS_TYPES)

class Results(models.Model):
    test1_result = models.CharField(max_length=3)

class ExaminationResult(models.Model):
    person_id = models.ForeignKey(ExaminedPerson, on_delete=models.CASCADE)
    exam_id = models.ForeignKey(Exam, on_delete=models.CASCADE, null=True)
    results_id = models.ForeignKey(Results, on_delete=models.CASCADE, null=True)
    start_date = models.DateTimeField('Start date', null=True)
    end_date = models.DateTimeField('End date', null=True)

    def __str__(self):
        return str(self.person_id) + ": " + str(self.start_date)


class AdminACC(models.Model):
    login = models.CharField(max_length=20)
    password = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)


class AdminToExam(models.Model):
    # Additional table for many to many Admin <-> Exam relation
    admin_id = models.ForeignKey(AdminACC, on_delete=models.CASCADE)
    exam_id = models.ForeignKey(Exam, on_delete=models.CASCADE)
    
    
class Fileset(models.Model):
    fileset_name = models.CharField(max_length=50)
    fileset_type = models.CharField(max_length=50)
    
    
class MUSHRATestSets(models.Model):
    fileset = models.ForeignKey(Fileset, on_delete=models.CASCADE)
    original_file_name = models.CharField(max_length=50)
    original_file_label = models.CharField(max_length=50)
    