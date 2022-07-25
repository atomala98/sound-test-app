from mainbackend.models import *
from time import time

start = time()

LOG_FILE = "q.txt"

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
        db_image[current] = []
    else:
        rec = load_dict(line)
        db_image[current].append(rec)

# queue = [
#     Test,
#     TestType,
#     ExaminedPerson,
#     Exam,
#     ExamTest,
#     ExaminationResult,
#     Result,
#     AdminACC,
#     AdminToExam,
#     Fileset,
#     FileDestination
# ]

queue = [
    FileDestination,
    Result
]



for model in queue:
    name = f'{model=}'.split('.')[-1][:-2]
    for rec in db_image[name]:
        try:
            db_object = model(**rec)
            db_object.save()
        except Exception as e:
            print(rec, e)

print(time() - start)