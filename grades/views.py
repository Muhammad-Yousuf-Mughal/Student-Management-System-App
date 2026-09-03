from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Avg, F, ExpressionWrapper, DecimalField, Q, Sum

from core.decorators import role_required
from grades.models import Mark
from grades.forms import MarkForm
from courses.models import Course
from students.models import Student

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


@method_decorator(login_required, name='dispatch')
class MarkListView(generic.ListView):
    model = Mark
    template_name = 'grades/mark_list.html'
    context_object_name = 'marks'
    paginate_by = 25

    def get_queryset(self):
        queryset = Mark.objects.select_related('student__user', 'course').all()
        course_filter = self.request.GET.get('course')
        if course_filter:
            queryset = queryset.filter(course_id=course_filter)
        search = self.request.GET.get('q')
        if search:
            queryset = queryset.filter(
                Q(student__user__first_name__icontains=search) |
                Q(student__user__last_name__icontains=search) |
                Q(course__name__icontains=search)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['courses'] = Course.objects.filter(is_active=True)
        return context


@method_decorator(login_required, name='dispatch')
class MarkCreateView(SuccessMessageMixin, generic.CreateView):
    model = Mark
    form_class = MarkForm
    template_name = 'grades/mark_form.html'
    success_message = 'Marks recorded successfully!'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial'] = {'exam_type': 'final', 'max_marks': 100}
        return kwargs


@method_decorator(login_required, name='dispatch')
class MarkUpdateView(SuccessMessageMixin, generic.UpdateView):
    model = Mark
    form_class = MarkForm
    template_name = 'grades/mark_form.html'
    success_message = 'Marks updated successfully!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mark'] = self.object
        return context


@method_decorator(login_required, name='dispatch')
class MarkDeleteView(SuccessMessageMixin, generic.DeleteView):
    model = Mark
    template_name = 'grades/mark_confirm_delete.html'
    success_url = reverse_lazy('grades:mark_list')
    success_message = 'Marks deleted successfully!'


@login_required
def student_results(request, pk):
    student = get_object_or_404(Student, pk=pk)
    marks = Mark.objects.filter(student=student).select_related('course')

    from django.db.models import Sum
    total_marks = marks.aggregate(
        total_obtained=Sum('marks_obtained'),
        total_max=Sum('max_marks')
    )
    total_obtained = total_marks['total_obtained'] or 0
    total_max = total_marks['total_max'] or 0
    overall_percentage = round((total_obtained / total_max * 100), 2) if total_max > 0 else 0

    course_stats = []
    for mark in marks:
        course_stats.append({
            'mark': mark,
            'percentage': mark.get_percentage(),
            'grade': mark.calculate_grade(),
        })

    context = {
        'student': student,
        'marks': course_stats,
        'total_obtained': total_obtained,
        'total_max': total_max,
        'overall_percentage': overall_percentage,
        'overall_grade': _get_overall_grade(overall_percentage),
    }
    return render(request, 'grades/student_results.html', context)


def _get_overall_grade(percentage):
    if percentage >= 90:
        return 'A+'
    elif percentage >= 80:
        return 'A'
    elif percentage >= 70:
        return 'B+'
    elif percentage >= 60:
        return 'B'
    elif percentage >= 50:
        return 'C+'
    elif percentage >= 40:
        return 'C'
    elif percentage >= 33:
        return 'D'
    else:
        return 'F'


@login_required
def course_marks(request, pk):
    course = get_object_or_404(Course, pk=pk)
    marks = Mark.objects.filter(course=course).select_related('student__user')

    percentage_expr = ExpressionWrapper(
        F('marks_obtained') / F('max_marks') * 100,
        output_field=DecimalField(max_digits=5, decimal_places=2)
    )
    avg_result = marks.aggregate(avg_percentage=Avg(percentage_expr))
    avg_percentage = round(avg_result['avg_percentage'], 2) if avg_result['avg_percentage'] is not None else 0

    student_marks = []
    for mark in marks:
        student_marks.append({
            'mark': mark,
            'percentage': mark.get_percentage(),
            'grade': mark.calculate_grade(),
        })

    context = {
        'course': course,
        'marks': student_marks,
        'avg_percentage': avg_percentage,
    }
    return render(request, 'grades/course_marks.html', context)


@login_required
def enter_marks_quick(request, course_pk):
    course = get_object_or_404(Course, pk=course_pk)
    exam_type = request.GET.get('exam_type', 'final')

    if request.method == 'POST':
        student_ids = request.POST.getlist('student_id')
        marks_obtained = request.POST.getlist('marks_obtained')
        max_marks = request.POST.getlist('max_marks')

        for sid, mo, mm in zip(student_ids, marks_obtained, max_marks):
            student = get_object_or_404(Student, id=sid)
            Mark.objects.update_or_create(
                student=student,
                course=course,
                exam_type=exam_type,
                defaults={
                    'marks_obtained': mo,
                    'max_marks': mm,
                }
            )
        messages.success(request, 'Marks saved successfully!')
        return redirect('grades:course_marks', pk=course_pk)

    enrolled_students = course.students.select_related('user').all()
    existing_marks = Mark.objects.filter(course=course, exam_type=exam_type).select_related('student')

    student_data = []
    for student in enrolled_students:
        existing = existing_marks.filter(student=student).first()
        student_data.append({
            'student': student,
            'existing_marks': existing.marks_obtained if existing else '',
            'existing_max': existing.max_marks if existing else 100,
        })

    context = {
        'course': course,
        'exam_type': exam_type,
        'students': student_data,
    }
    return render(request, 'grades/quick_entry.html', context)
