from django.urls import path
from core import views as core_views
from core import dashboard as core_dashboard

app_name = 'core'

urlpatterns = [
    path('', core_dashboard.dashboard, name='dashboard'),
]
