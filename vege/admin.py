from django.contrib import admin
from .models import *


class StudentAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return Student.admin_objects.all()


admin.site.register(Receipe)
admin.site.register(StudentID)
admin.site.register(Student, StudentAdmin)
admin.site.register(Department)
admin.site.register(Subject)
admin.site.register(SubjectMarks)
admin.site.register(ReportCard)