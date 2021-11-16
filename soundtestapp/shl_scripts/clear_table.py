from mainbackend.models import *

name = "Exam"

exec(f"{name}.objects.all().delete()")
