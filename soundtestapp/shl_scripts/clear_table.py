from mainbackend.models import *

name = "Result"

exec(f"{name}.objects.all().delete()")
