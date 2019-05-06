from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView
from .models import Student, Attendance


def home(request):
    return render(request, 'facematch/home.html')


def about(request):
    return render(request, 'facematch/about.html')


def confirm(request):
    context = {
        'student_data': student_data,
        'title': 'Confirm'
    }
    return render(request, 'facematch/confirm.html', context)


def upload(request):
    return render(request, 'facematch/upload.html')


class StudentCreateView(LoginRequiredMixin, CreateView):
    model = Student
    template_name = 'facematch/student.html'

    fields = ['rollno', 'name', 'program', 'semester', 'section', 'image']


class AttendanceCreateView(LoginRequiredMixin, CreateView):
    model = Attendance
    template_name = 'facematch/attendance.html'

    fields = ['date', 'starttime', 'endtime', 'subject']
