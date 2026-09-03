from django.contrib import messages
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Q

from core.decorators import teacher_required, admin_required
from attendance.models import Attendance
from attendance.forms import AttendanceForm, AttendanceBulkForm
from courses.models import Course
from students.models import Student

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


@method_decorator(login_required, name='dispatch')
class AttendanceListView(generic.ListView):
    model = Attendance
    template_name = 'attendance/attendance_list.html'
    context_object_name = 'attendances'
    paginate_by = 25

    def get_queryset(self):
        queryset = Attendance.objects.select_related('student__user', 'course').all()
        course_filter = self.request.GET.get('course')
        date_filter = self.request.GET.get('date')
        if course_filter:
            queryset = queryset.filter(course_id=course_filter)
        if date_filter:
            queryset = queryset.filter(date=date_filter)
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
class AttendanceDetailView(generic.DetailView):
    model = Attendance
    template_name = 'attendance/attendance_detail.html'
    context_object_name = 'attendance'
    pk_url_kwarg = 'pk'


@login_required
def mark_attendance(request):
    if request.method == 'POST':
        form = AttendanceBulkForm(request.POST)
        if form.is_valid():
            course = form.cleaned_data['course']
            date = form.cleaned_data['date']
            status_list = request.POST.getlist('status')
            student_ids = request.POST.getlist('student_id')
            remarks = form.cleaned_data['remarks']

            for student_id, status in zip(student_ids, status_list):
                student = get_object_or_404(Student, id=student_id)
                Attendance.objects.update_or_create(
                    student=student,
                    course=course,
                    date=date,
                    defaults={'status': status, 'remarks': remarks},
                )
            messages.success(request, f'Attendance marked for {len(status_list)} student(s) on {date}!')
            return redirect('attendance:list')
    else:
        form = AttendanceBulkForm()

    course_id = request.GET.get('course')
    date = request.GET.get('date')
    selected_course = None
    students = Student.objects.none()

    if course_id:
        selected_course = get_object_or_404(Course, id=course_id)
        students = selected_course.students.select_related('user').all()
    elif date:
        pass

    context = {
        'form': form,
        'selected_course': selected_course,
        'students': students,
        'courses': Course.objects.filter(is_active=True),
    }
    return render(request, 'attendance/mark_attendance.html', context)


@login_required
def attendance_report(request, pk):
    course = get_object_or_404(Course, pk=pk)
    attendances = Attendance.objects.filter(course=course).select_related('student__user')

    total = attendances.count()
    present = attendances.filter(status=Attendance.Status.PRESENT).count()
    absent = attendances.filter(status=Attendance.Status.ABSENT).count()
    late = attendances.filter(status=Attendance.Status.LATE).count()

    overall_percentage = round((present / total * 100), 2) if total > 0 else 0

    student_stats = attendances.values('student').annotate(
        total=Count('id'),
        present_count=Count('id', filter=Q(status=Attendance.Status.PRESENT)),
    ).order_by('student')

    from django.db.models import F
    student_list = []
    for stat in student_stats:
        student = Student.objects.get(id=stat['student'])
        total_days = stat['total']
        present_days = stat['present_count']
        percentage = round((present_days / total_days * 100), 2) if total_days > 0 else 0
        student_list.append({
            'student': student,
            'total_days': total_days,
            'present_days': present_days,
            'percentage': percentage,
        })

    context = {
        'course': course,
        'total_records': total,
        'present_count': present,
        'absent_count': absent,
        'late_count': late,
        'overall_percentage': overall_percentage,
        'student_stats': student_list,
    }
    return render(request, 'attendance/report.html', context)
