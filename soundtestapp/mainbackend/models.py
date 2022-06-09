from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.hashers import check_password
import uuid
import json

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
        return str(self.first_name) + " " + str(self.last_name)


class Test(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=10000, null=True)
    function = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return str(self.name)


class TestType(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, null=True)
    question = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return str(self.name)


def create_invite_code():
    return str(uuid.uuid4())[0:8]


class Exam(models.Model):
    exam_name = models.CharField(max_length=30, null=True)
    test_amount = models.IntegerField(null=True)
    STATUS_TYPES = (
        ('W', 'Waiting for parameters'),
        ('O', 'Open'),
        ('C', 'Close')
    )
    status = models.CharField(max_length=1, choices=STATUS_TYPES)
    exam_code = models.CharField(max_length=6, null=True, default=create_invite_code, unique=True)
   
    def toJSON(self):
        return {
            "exam_id": self.id,
            "exam_name": self.exam_name,
            "test_amount": self.test_amount
        }
   

class ExamTest(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    test_number = models.DecimalField(max_digits=1, decimal_places=0, null=True)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    parameter_1 = models.CharField(max_length=30, null=True)
    parameter_2 = models.CharField(max_length=30, null=True)
    parameter_3 = models.CharField(max_length=30, null=True)
    parameter_4 = models.CharField(max_length=30, null=True)
    parameter_5 = models.CharField(max_length=30, null=True)
    
    def __str__(self):
        return str(self.exam.exam_name) + ' ' + str(self.test.name)
    
    def redirect(self):
        return str(self.test.name)
    
    def toJSON(self):
        json_dump = {
            "test_id": self.id,
            "test_number": int(self.test_number),
            "parameter_1": self.parameter_1,
            "parameter_2": self.parameter_2,
            "parameter_3": self.parameter_3,
            "parameter_4": self.parameter_4,
            "parameter_5": self.parameter_5,
            "iteration": 1
        }
        return json_dump


class ExaminationResult(models.Model):
    person_id = models.ForeignKey(ExaminedPerson, on_delete=models.CASCADE)
    exam_id = models.ForeignKey(Exam, on_delete=models.CASCADE, null=True)
    start_date = models.DateTimeField('Start date', null=True)
    end_date = models.DateTimeField('End date', null=True)
    STATUS_TYPES = (
        ('T', 'True'),
        ('F', 'False')
    )
    exam_finished = models.CharField(max_length=1, choices=STATUS_TYPES, null=True)

    def __str__(self):
        return str(self.person_id) + ": " + str(self.start_date)


class Result(models.Model):
    examination_result = models.ForeignKey(ExaminationResult, on_delete=models.CASCADE)
    exam_test = models.ForeignKey(ExamTest, on_delete=models.CASCADE)
    result = models.CharField(max_length=30, null=True)
    result_number = models.DecimalField(max_digits=2, decimal_places=0, null=True)


class AdminACC(models.Model):
    login = models.CharField(max_length=20)
    password = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)


class AdminToExam(models.Model):
    # Additional table for many to many Admin <-> Exam relation
    admin = models.ForeignKey(AdminACC, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    
    
class Fileset(models.Model):
    fileset_name = models.CharField(max_length=50, unique=True)
    fileset_type = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=2, decimal_places=0, null=True)
    file_labels = models.CharField(max_length=1000, null=True)
    
    def __str__(self):
        return str(self.fileset_name)
    
    
class FileDestination(models.Model):
    fileset = models.ForeignKey(Fileset, on_delete=models.CASCADE)
    filename = models.CharField(max_length=150)
    file_label = models.CharField(max_length=150)
    file_destination = models.CharField(max_length=150)
    file_number = models.DecimalField(max_digits=2, decimal_places=0, null=True)