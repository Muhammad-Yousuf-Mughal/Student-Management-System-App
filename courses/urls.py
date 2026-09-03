from django.urls import path
from courses import views

app_name = 'courses'

urlpatterns = [
    path('', views.CourseListView.as_view(), name='course_list'),
    path('add/', views.CourseCreateView.as_view(), name='course_add'),
    path('departments/', views.DepartmentListView.as_view(), name='department_list'),
    path('<int:pk>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('<int:pk>/edit/', views.CourseUpdateView.as_view(), name='course_edit'),
    path('<int:pk>/delete/', views.CourseDeleteView.as_view(), name='course_delete'),
    path('<int:pk>/enroll/', views.enroll_student, name='enroll_student'),
    path('<int:pk>/bulk-enroll/', views.bulk_enroll_students, name='bulk_enroll'),
    path('<int:course_pk>/unenroll/<int:enrollment_pk>/', views.unenroll_student, name='unenroll_student'),
]
