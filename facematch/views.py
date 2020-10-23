from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required

from django.utils.dateparse import parse_date
from .models import Student, Attendance, TempFile
from .forms import UploadFileForm, AttendanceForm, GetDataForm
from .utils import identify

from .filters import StudentFilter, AttendanceFilter


def home(request):
    return render(request, 'facematch/home.html')


def about(request):
    return render(request, 'facematch/about.html')


class StudentCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Student
    template_name = 'facematch/student.html'
    success_url = '/'
    success_message = "%(name)s is added successfully."

    fields = ['rollno', 'name', 'program', 'semester', 'section', 'image']


@login_required
def getData(request):
    if request.method == 'POST':
        form = GetDataForm(request.POST)
        if form.is_valid():
            # form.save()
            program = form.cleaned_data.get('program')
            section = form.cleaned_data.get('section')
            semester = form.cleaned_data.get('semester')
            request.session['program'] = program
            request.session['section'] = section
            request.session['semester'] = semester

            messages.success(request, 'Please Provide Details for marking attendance.')
            return redirect('facematch-attendance-info')
    else:
        form = GetDataForm()

    context = {
        'form': form
    }

    return render(request, 'facematch/attendance_getdata.html', context)


@login_required
def info(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            program = request.session.get('program')
            section = request.session.get('section')
            semester = request.session.get('semester')
            student_data = Student.objects.filter(program=program, section=section, semester=semester).order_by('rollno')

            if student_data:
                lecture = form.cleaned_data.get('lecture')
                date = str(form.cleaned_data.get('date'))
                subject = form.cleaned_data.get('subject')

                request.session['lecture'] = lecture
                request.session['date'] = date
                request.session['subject'] = subject

                messages.success(request, 'Please Upload Image File to mark attendance')
                return redirect('facematch-attendance-upload')

            # Else case
            messages.warning(request, 'Opps, No Student Record Found')
            return redirect('facematch-attendance-getdata')

    else:
        form = AttendanceForm()

    context = { 'form': form }
    return render(request, 'facematch/attendance_info.html', context)


@login_required
def upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            file_name = form.cleaned_data.get('image')

            program = request.session.get('program')
            section = request.session.get('section')
            semester = request.session.get('semester')
            student_data = Student.objects.filter(program=program, section=section, semester=semester)

            # Recognition Function
            try:
                processed_student_data = identify(student_data, file_name)
                # processed_student_data = sorted(processed_student_data)
                request.session["student_data"] = processed_student_data
            except FileNotFoundError:
                messages.warning(request, 'ATTENDANCE NOT MARKED!! Some Images are missing, Please contact Admin.')
                return redirect("facematch-home")
            #Delete in DB
            TempFile.objects.filter(image=f'raw_files/{file_name}').delete()
            messages.success(request, 'Please Confirm!!')
            return redirect('facematch-confirm')
    else:
        form = UploadFileForm()

    context = {
        'form': form
    }

    return render(request, 'facematch/attendance_upload.html', context)


def confirm(request):
    student_data = request.session.get('student_data')
    if request.method == 'POST':
        lecture = request.session.get('lecture')
        date = parse_date(request.session.get('date'))
        subject = request.session.get('subject')

        # Saving data to DB.
        for key, value in student_data.items():
            attn = Attendance(attendance=value, lecture=lecture, subject=subject, date=date,
                              student=Student.objects.get(id=key))
            attn.save()
        messages.success(request, 'Attendance marked Successfully.')
        return redirect('facematch-home')

    view_data = {}

    for key, value in student_data.items():
        student = Student.objects.get(id=key)
        view_data[key] = {
            'roll': student.rollno,
            'name': student.name,
            'attendance': value
        }
    context = {
        'view_data': view_data
    }
    return render(request, 'facematch/confirm.html', context)


def report(request):
    return render(request, 'facematch/report.html')


# Report Filtering
def studentReport(request):
    student_list = Student.objects.all().order_by('rollno')
    student_filter = StudentFilter(request.GET, queryset=student_list)

    return render(request, 'facematch/student_report_new.html', {'filter': student_filter})


def attendanceReport(request):
    attendance_list = Attendance.objects.all().order_by('student')
    attendance_filter = AttendanceFilter(request.GET, queryset=attendance_list)

    return render(request, 'facematch/student_attendance_report.html', {'filter': attendance_filter})
