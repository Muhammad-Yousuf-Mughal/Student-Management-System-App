from django.urls import path
from teachers import views

app_name = 'teachers'

urlpatterns = [
    path('', views.TeacherListView.as_view(), name='teacher_list'),
    path('add/', views.TeacherCreateView.as_view(), name='teacher_add'),
    path('<int:pk>/', views.TeacherDetailView.as_view(), name='teacher_detail'),
    path('<int:pk>/edit/', views.TeacherUpdateView.as_view(), name='teacher_edit'),
    path('<int:pk>/delete/', views.TeacherDeleteView.as_view(), name='teacher_delete'),
]
