# from django.contrib.auth.models import User
from .models import Student, Attendance
import django_filters


class StudentFilter(django_filters.FilterSet):
    class Meta:
        model = Student
        fields = ['rollno', 'name', 'program', 'semester', 'section']

    def __init__(self, *args, **kwargs):
        super(StudentFilter, self).__init__(*args, **kwargs)
        # at startup user doesn't push Submit button, and QueryDict (in data) is empty
        if self.data == {}:
            self.queryset = self.queryset.none()


class AttendanceFilter(django_filters.FilterSet):
    class Meta:
        model = Attendance
        fields = ['date' , 'lecture' , 'subject', 'student', 'attendance']

    def __init__(self, *args, **kwargs):
        """
        At startup user doesn't push submit button, and QueryDict (in data) is empty
        """
        super(AttendanceFilter, self).__init__(*args, **kwargs)
        if self.data == {}:
            self.queryset = self.queryset.none()
