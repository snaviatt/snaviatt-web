from django import forms
from .models import Attendance, TempFile


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['date', 'lecture', 'subject']


class UploadFileForm(forms.ModelForm):
    class Meta:
        model = TempFile
        fields = ['image']


class GetDataForm(forms.Form):
    program = forms.CharField()
    semester = forms.IntegerField()
    section = forms.CharField(max_length=1)
