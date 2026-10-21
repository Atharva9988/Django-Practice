from django.contrib import admin
from .models import Receipe
from .models import *

admin.site.register(Receipe)

admin.site.register(StudentID)
admin.site.register(Student)
admin.site.register(Department)