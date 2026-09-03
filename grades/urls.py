from django.urls import path
from grades import views

app_name = 'grades'

urlpatterns = [
    path('', views.MarkListView.as_view(), name='mark_list'),
    path('add/', views.MarkCreateView.as_view(), name='mark_add'),
    path('<int:pk>/edit/', views.MarkUpdateView.as_view(), name='mark_edit'),
    path('<int:pk>/delete/', views.MarkDeleteView.as_view(), name='mark_delete'),
    path('student/<int:pk>/', views.student_results, name='student_results'),
    path('course/<int:pk>/', views.course_marks, name='course_marks'),
    path('course/<int:course_pk>/quick-entry/', views.enter_marks_quick, name='quick_entry'),
]
