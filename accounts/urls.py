from django.urls import path
from core import views as core_views

app_name = 'accounts'

urlpatterns = [
    path('login/', core_views.login_view, name='login'),
    path('logout/', core_views.logout_view, name='logout'),
    path('register/', core_views.register_view, name='register'),
    path('profile/', core_views.profile_view, name='profile'),
]
