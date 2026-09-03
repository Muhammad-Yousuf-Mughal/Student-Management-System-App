from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from functools import wraps


def role_required(roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                from django.shortcuts import redirect
                return redirect('login')
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            if hasattr(request.user, 'role') and request.user.role in roles:
                return view_func(request, *args, **kwargs)
            from django.http import HttpResponseForbidden
            return HttpResponseForbidden()
        return _wrapped_view
    return decorator


def admin_required(view_func=None):
    actual_decorator = role_required(['admin'])
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator


def teacher_required(view_func=None):
    actual_decorator = role_required(['admin', 'teacher'])
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator


def student_required(view_func=None):
    actual_decorator = role_required(['admin', 'student'])
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator


class RoleRequiredMixin(UserPassesTestMixin):
    roles = []

    def get_roles(self):
        return self.roles

    def test_func(self):
        user = self.request.user
        if not user.is_authenticated:
            return False
        if user.is_superuser:
            return True
        if hasattr(user, 'role') and user.role in self.get_roles():
            return True
        return False


class AdminRequiredMixin(RoleRequiredMixin):
    roles = ['admin']


class TeacherRequiredMixin(RoleRequiredMixin):
    roles = ['admin', 'teacher']


class StudentRequiredMixin(RoleRequiredMixin):
    roles = ['admin', 'student']
