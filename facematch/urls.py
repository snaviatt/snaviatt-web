from django.urls import path
from .views import StudentCreateView, AttendanceCreateView
from . import views

urlpatterns = [
    path('', views.home, name='facematch-home'),
    path('confirm/', views.confirm, name='facematch-confirm'),
    path('about/', views.about, name='facematch-about'),
    path('upload/', views.upload, name='facematch-upload'),
    path('new/student/', StudentCreateView.as_view(), name='facematch-student'),
    path('attendance/', AttendanceCreateView.as_view(), name='facematch-attendance'),
]
