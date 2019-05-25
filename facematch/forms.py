from django import forms
from .models import Student, Attendance, TempFile


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
    # file = forms.ImageField()  # widget=forms.FileInput(attrs={'accept':'application/image', }))

    # class Meta:
    #     model = Attendance
    #     fields = AttendanceForm.Meta.fields + ['program', 'semester', 'section', 'file']  # + UploadFileForm.Meta.fields


# class ConfirmForm(forms.Form):
