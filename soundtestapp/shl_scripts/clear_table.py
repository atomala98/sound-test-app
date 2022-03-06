from mainbackend.models import *

name = "Fileset"

exec(f"{name}.objects.all().delete()")
