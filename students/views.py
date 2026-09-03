from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q

from accounts.models import User
from core.decorators import admin_required
from students.models import Student
from students.forms import StudentForm

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


@method_decorator(login_required, name='dispatch')
class StudentListView(generic.ListView):
    model = Student
    template_name = 'students/student_list.html'
    context_object_name = 'students'
    paginate_by = 25

    def get_queryset(self):
        queryset = Student.objects.select_related('user').all()
        search = self.request.GET.get('q')
        if search:
            queryset = queryset.filter(
                Q(user__first_name__icontains=search) |
                Q(user__last_name__icontains=search) |
                Q(student_id__icontains=search) |
                Q(user__email__icontains=search)
            )
        return queryset


@method_decorator(login_required, name='dispatch')
class StudentDetailView(generic.DetailView):
    model = Student
    template_name = 'students/student_detail.html'
    context_object_name = 'student'
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = self.object
        context['enrollments'] = student.get_enrolled_courses()
        from grades.models import Mark
        context['marks'] = Mark.objects.filter(student=student).select_related('course')
        from attendance.models import Attendance
        context['recent_attendance'] = Attendance.objects.filter(student=student).order_by('-date')[:10]
        context['attendance_percentage'] = student.get_attendance_percentage()
        return context


@method_decorator([login_required], name='dispatch')
class StudentCreateView(SuccessMessageMixin, generic.CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'students/student_form.html'
    success_message = 'Student created successfully!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from students.forms import StudentRegistrationForm
        context['registration_form'] = StudentRegistrationForm()
        return context

    def post(self, request, *args, **kwargs):
        from students.forms import StudentRegistrationForm
        self.object = None
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'first_name': form.cleaned_data['first_name'],
                    'last_name': form.cleaned_data['last_name'],
                    'role': User.Role.STUDENT,
                }
            )
            if created:
                user.set_password('Student@123')
                user.save()
            student = Student.objects.create(
                user=user,
                student_id=form.cleaned_data['student_id'],
                date_of_birth=form.cleaned_data.get('date_of_birth'),
                grade_level=form.cleaned_data.get('grade_level', ''),
                parent_guardian=form.cleaned_data.get('parent_guardian', ''),
                parent_phone=form.cleaned_data.get('parent_phone', ''),
            )
            messages.success(request, f'Student {student.user.get_full_name()} created! Default password: Student@123')
            return redirect('students:student_detail', pk=student.pk)
        else:
            context = self.get_context_data()
            context['form'] = form
            return render(request, self.template_name, context)


@method_decorator([login_required], name='dispatch')
class StudentUpdateView(SuccessMessageMixin, generic.UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'students/student_form.html'
    success_message = 'Student updated successfully!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['student'] = self.object
        return context


@method_decorator([login_required], name='dispatch')
class StudentDeleteView(SuccessMessageMixin, generic.DeleteView):
    model = Student
    template_name = 'students/student_confirm_delete.html'
    success_url = reverse_lazy('students:student_list')
    success_message = 'Student deleted successfully!'
