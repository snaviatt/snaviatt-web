from django.contrib import admin
from .models import Student, Attendance, TempFile

# Register your Models here.
admin.site.register(Student)
admin.site.register(Attendance)
admin.site.register(TempFile)
