from mainbackend.models import *
from datetime import datetime
from time import strftime, gmtime
import os
from time import time

start = time()

dt_gmt = strftime("logs\db_state\%Y-%m-%d_%H-%M-%S", gmtime())

def flatten(rec):
    out = []
    for key, val in rec.__dict__.items():
        if key != '_state':
            if type(val) == str:
                val = val.replace('\n', '\\n')
            out.append(f'{key} -> {val}')
    return "LOG: " + " | ".join(out)

queue = [
    Test,
    TestType,
    ExaminedPerson,
    Exam,
    ExamTest,
    ExaminationResult,
    Result,
    AdminACC,
    AdminToExam,
    Fileset,
    FileDestination
]

with open(f'{dt_gmt}_log.txt', 'w') as logs:
    for model in queue:
        name = f'{model=}'.split('.')[-1][:-2]
        logs.write(name + "\n")
        for rec in model.objects.all():
            logs.write(flatten(rec) + "\n")  
        logs.write('\n')
        
print(time() - start)