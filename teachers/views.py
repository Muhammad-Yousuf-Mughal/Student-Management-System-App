from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import generic
from django.db.models import Q
from django.shortcuts import render, redirect

from core.decorators import admin_required, teacher_required
from teachers.models import Teacher
from teachers.forms import TeacherForm

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


@method_decorator(login_required, name='dispatch')
class TeacherListView(generic.ListView):
    model = Teacher
    template_name = 'teachers/teacher_list.html'
    context_object_name = 'teachers'
    paginate_by = 25

    def get_queryset(self):
        queryset = Teacher.objects.select_related('user').all()
        search = self.request.GET.get('q')
        if search:
            queryset = queryset.filter(
                Q(user__first_name__icontains=search) |
                Q(user__last_name__icontains=search) |
                Q(employee_id__icontains=search) |
                Q(user__email__icontains=search)
            )
        return queryset


@method_decorator(login_required, name='dispatch')
class TeacherDetailView(generic.DetailView):
    model = Teacher
    template_name = 'teachers/teacher_detail.html'
    context_object_name = 'teacher'
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        teacher = self.object
        context['courses'] = teacher.get_assigned_courses().select_related('department')
        return context


@method_decorator([login_required], name='dispatch')
class TeacherCreateView(SuccessMessageMixin, generic.CreateView):
    model = Teacher
    form_class = TeacherForm
    template_name = 'teachers/teacher_form.html'
    success_message = 'Teacher created successfully!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['show_user_fields'] = True
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', 'Teacher@123')

        if not (first_name and last_name and email):
            from teachers.forms import TeacherForm
            form = TeacherForm(request.POST)
            context = self.get_context_data()
            context['form'] = form
            context['error'] = 'First name, last name, and email are required.'
            return render(request, self.template_name, context)

        from accounts.models import User
        user, created = User.objects.get_or_create(
            email=email,
            defaults={'first_name': first_name, 'last_name': last_name, 'role': User.Role.TEACHER}
        )
        if created:
            user.set_password(password)
            user.save()
        else:
            user.role = User.Role.TEACHER
            user.save()

        from teachers.forms import TeacherForm
        form = TeacherForm(request.POST)
        if form.is_valid():
            teacher = form.save(commit=False)
            teacher.user = user
            teacher.save()
            messages.success(request, f'Teacher {teacher.user.get_full_name()} created!')
            return redirect('teachers:teacher_detail', pk=teacher.pk)
        else:
            context = self.get_context_data()
            context['form'] = form
            return render(request, self.template_name, context)


@method_decorator([login_required], name='dispatch')
class TeacherUpdateView(SuccessMessageMixin, generic.UpdateView):
    model = Teacher
    form_class = TeacherForm
    template_name = 'teachers/teacher_form.html'
    success_message = 'Teacher updated successfully!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['teacher'] = self.object
        return context


@method_decorator([login_required], name='dispatch')
class TeacherDeleteView(SuccessMessageMixin, generic.DeleteView):
    model = Teacher
    template_name = 'teachers/teacher_confirm_delete.html'
    success_url = reverse_lazy('teachers:teacher_list')
    success_message = 'Teacher deleted successfully!'
