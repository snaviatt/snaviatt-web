from django.db import models

# from django.utils import timezone
from PIL import Image
from datetime import date


class Student(models.Model):
    rollno = models.PositiveIntegerField()
    name = models.CharField(max_length=100)
    program = models.CharField(max_length=50)
    semester = models.PositiveIntegerField()
    section = models.CharField(max_length=2)
    image = models.ImageField(upload_to='students_pics')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Attendance(models.Model):
    attendance = models.BooleanField(default=False)
    date = models.DateField(default=date.today)
    lecture = models.SmallIntegerField()
    # starttime = models.TimeField()
    # endtime = models.TimeField()
    subject = models.CharField(max_length=50)
    student = models.ForeignKey(Student, on_delete=models.PROTECT)

    def __str__(self):
        return self.student.name


class TempFile(models.Model):
    image = models.ImageField(upload_to='raw_files')

    def __str__(self):
        return self.image.url
