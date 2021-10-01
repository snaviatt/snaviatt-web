from django.urls import path
from .views import StudentCreateView  # AttendanceCreateView
from . import views


urlpatterns = [
    path('', views.home, name='facematch-home'),
    path('confirm/', views.confirm, name='facematch-confirm'),
    path('about/', views.about, name='facematch-about'),
    # path('upload/', views.upload, name='facematch-upload'),
    path('new/student/', StudentCreateView.as_view(), name='facematch-student'),
    # path('attendance/', AttendanceCreateView.as_view(), name='facematch-attendance'),
    path('attendance/info', views.info, name='facematch-attendance-info'),
    path('attendance/getdata', views.getData, name='facematch-attendance-getdata'),
    path('attendance/upload', views.upload, name='facematch-attendance-upload'),
    # Filtering routes
    path('report/student', views.studentReport, name='facematch-report-student'),
    path('report/attendance', views.attendanceReport, name='facematch-report-attendance'),
    path('report', views.report, name='facematch-report'),
]

handler404 = 'facematch.views.handler404'
handler500 = 'facematch.views.handler500'
