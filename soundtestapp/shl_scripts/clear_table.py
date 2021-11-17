from mainbackend.models import *

name = "Test"

exec(f"{name}.objects.all().delete()")
