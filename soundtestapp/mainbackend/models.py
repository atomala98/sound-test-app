from django.db import models

# Create your models here.

class ExaminationResult(models.Model):
    person_id = models.IntegerField()
    start_date = models.DateTimeField('Start date')
    end_date = models.DateTimeField('End date')

    def __str__(self):
        return str(self.person_id) + ": " + str(self.start_date)