from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView
from django.contrib.auth.decorators import login_required

from django.utils.dateparse import parse_date
from .models import Student, Attendance, TempFile
from .forms import UploadFileForm, AttendanceForm, GetDataForm
from .utils import identify


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


# class AttendanceCreateView(LoginRequiredMixin, CreateView):
#     model = Attendance
#     template_name = 'facematch/attendance.html'

#     fields = ['date', 'lecture', 'subject']

    # def form_valid(self, form):
    #     form.instance.created_by = self.request.user
    #     return super().form_valid(form)

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
            # student_data = Student.objects.filter(program=program, section=section, semester=semester)

            # if student_data:
            #     print("Yes")
            #     # identify(student_data)
            # else:
            #     messages.warning(request, f'There are no students available for given data.')

            messages.success(request, f'Please Provide Details for marking attendance.')
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
            student_data = Student.objects.filter(program=program, section=section, semester=semester)

            if student_data:
                lecture = form.cleaned_data.get('lecture')
                date = str(form.cleaned_data.get('date'))
                subject = form.cleaned_data.get('subject')

                request.session['lecture'] = lecture
                request.session['date'] = date
                request.session['subject'] = subject

                messages.success(request, f'Please Upload Image/Video to mark attendance. ')
                return redirect('facematch-attendance-upload')
            else:
                messages.warning(request, f'Opps, No Student Record Found')
                return redirect('facematch-attendance-getdata')

    else:
        form = AttendanceForm()

    context = {
        'form': form
    }

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
            processed_student_data = identify(student_data, file_name)
            request.session["student_data"] = processed_student_data
            #Delete in DB
            TempFile.objects.filter(image=f'raw_files/{file_name}').delete()
            messages.success(request, f'Please Confirm!!')
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
        messages.success(request, f'Attendance marked Successfully.')
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
