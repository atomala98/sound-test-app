from mainbackend.models import *

name = "Person"

exec(f"{name}.objects.all().delete()")
