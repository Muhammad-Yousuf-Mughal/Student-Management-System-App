from django.urls import path
from attendance import views

app_name = 'attendance'

urlpatterns = [
    path('', views.AttendanceListView.as_view(), name='list'),
    path('mark/', views.mark_attendance, name='mark'),
    path('<int:pk>/', views.AttendanceDetailView.as_view(), name='detail'),
    path('report/<int:pk>/', views.attendance_report, name='report'),
]
