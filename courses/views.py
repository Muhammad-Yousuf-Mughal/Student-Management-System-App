from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import generic
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from core.decorators import admin_required
from courses.models import Course, Department, Enrollment
from courses.forms import CourseForm, DepartmentForm, EnrollmentForm

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


@method_decorator(login_required, name='dispatch')
class CourseListView(generic.ListView):
    model = Course
    template_name = 'courses/course_list.html'
    context_object_name = 'courses'
    paginate_by = 25

    def get_queryset(self):
        queryset = Course.objects.select_related('department', 'teacher').all()
        search = self.request.GET.get('q')
        if search:
            queryset = queryset.filter(
                Q(course_code__icontains=search) |
                Q(name__icontains=search) |
                Q(description__icontains=search)
            )
        return queryset


@method_decorator(login_required, name='dispatch')
class CourseDetailView(generic.DetailView):
    model = Course
    template_name = 'courses/course_detail.html'
    context_object_name = 'course'
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.object
        context['enrollments'] = course.enrollments.select_related('student__user').all()
        from attendance.models import Attendance
        context['attendances'] = Attendance.objects.filter(course=course).select_related('student__user')[:20]
        from grades.models import Mark
        context['marks'] = Mark.objects.filter(course=course).select_related('student__user')
        return context


@method_decorator([login_required], name='dispatch')
class CourseCreateView(SuccessMessageMixin, generic.CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'courses/course_form.html'
    success_message = 'Course created successfully!'


@method_decorator([login_required], name='dispatch')
class CourseUpdateView(SuccessMessageMixin, generic.UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'courses/course_form.html'
    success_message = 'Course updated successfully!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = self.object
        return context


@method_decorator([login_required], name='dispatch')
class CourseDeleteView(SuccessMessageMixin, generic.DeleteView):
    model = Course
    template_name = 'courses/course_confirm_delete.html'
    success_url = reverse_lazy('courses:course_list')
    success_message = 'Course deleted successfully!'


@login_required
def enroll_student(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Student enrolled in {course.name} successfully!')
            return redirect('courses:course_detail', pk=pk)
    else:
        form = EnrollmentForm()
    return render(request, 'courses/enroll_student.html', {'form': form, 'course': course})


@login_required
def bulk_enroll_students(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        student_ids = request.POST.getlist('students')
        for student_id in student_ids:
            Enrollment.objects.get_or_create(student_id=student_id, course=course)
        messages.success(request, f'{len(student_ids)} student(s) enrolled in {course.name}!')
        return redirect('courses:course_detail', pk=pk)
    from students.models import Student
    enrolled_ids = course.students.values_list('id', flat=True)
    available_students = Student.objects.exclude(id__in=enrolled_ids)
    return render(request, 'courses/bulk_enroll.html', {
        'course': course,
        'students': available_students,
    })


@login_required
def unenroll_student(request, course_pk, enrollment_pk):
    enrollment = get_object_or_404(Enrollment, pk=enrollment_pk, course_id=course_pk)
    enrollment.delete()
    messages.info(request, 'Student unenrolled successfully!')
    return redirect('courses:course_detail', pk=course_pk)


@method_decorator(login_required, name='dispatch')
class DepartmentListView(generic.ListView):
    model = Department
    template_name = 'courses/department_list.html'
    context_object_name = 'departments'
