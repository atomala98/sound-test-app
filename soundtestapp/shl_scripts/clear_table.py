from mainbackend.models import *

name = "TestType"

exec(f"{name}.objects.all().delete()")
