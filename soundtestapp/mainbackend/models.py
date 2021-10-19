from django.db import models
from django.db.models.deletion import CASCADE


class ExaminedPerson(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    start_date = models.DateTimeField('Birth date')
    GENDERS = (
        ('M', 'Male'),
        ('F', 'Female')
    )
    gender = models.CharField(max_length=1, choices=GENDERS)

    def __str__(self):
        return str(self.first_name) + " " + str(self.last_name) + "."


class Test(models.Model):
    test_name = models.CharField(max_length=100)

    def __str__(self):
        return "Test: " + str(self.test_name)


class Exam(models.Model):
    exam_name = models.CharField(max_length=30, null=True)
    test_id = models.ForeignKey(Test, on_delete=models.CASCADE)


class ExaminationResult(models.Model):
    person_id = models.ForeignKey(ExaminedPerson, on_delete=models.CASCADE)
    exam_id = models.ForeignKey(Exam, on_delete=models.CASCADE, null=True)
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
    