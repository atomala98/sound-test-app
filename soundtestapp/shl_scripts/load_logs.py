from mainbackend.models import *
from time import time

start = time()

LOG_FILE = "fake25.txt"

path = f"logs\db_state\{LOG_FILE}"

file = open(path)

db_image = {}
current = ''


def load_dict(line):
    line = line[5:]
    line = list(map(lambda a: tuple(a.split(" -> ")), line.split(' | ')))
    line = {key.replace("'", '').strip(): value for key, value in line}
    return line


for line in file.read().splitlines():
    if not line:
        continue
    elif line[:4] != 'LOG:':
        current = line
        db_image[current] = {}
    else:
        rec = load_dict(line)
        db_image[current][rec['id']] = rec

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


for model in queue:
    name = f'{model=}'.split('.')[-1][:-2]
    for id, rec in db_image[name].items():
        try:
            db_object = model(**rec)
            db_object.save()
        except Exception as e:
            print(rec, e)

print(time() - start)