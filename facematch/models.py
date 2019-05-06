from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Student(models.Model):
    rollno = models.PositiveIntegerField()
    name = models.CharField(max_length=100)
    program = models.CharField(max_length=50)
    semester = models.PositiveIntegerField()
    section = models.CharField(max_length=2)
    image = models.ImageField(default='unknown.jpg', upload_to='students_pics')
    # image_path = models.FilePathField(path=os.join(MEDIA_ROOT, 'students'), match='*.[jpg, jpeg, png]', recursive=True)
    # teacher = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class Attendance(models.Model):
    attendance = models.BooleanField(default=False)
    date = models.DateTimeField(default=timezone.now)
    starttime = models.TimeField()
    endtime = models.TimeField()
    subject = models.CharField(max_length=50)
    student = models.ForeignKey(Student, on_delete=models.PROTECT)

    def __str__(self):
        return self.student.name
