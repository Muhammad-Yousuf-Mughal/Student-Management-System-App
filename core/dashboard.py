from django.contrib.auth.decorators import login_required
from django.db.models import Avg, F, DecimalField, ExpressionWrapper
from django.shortcuts import render

from accounts.models import User
from students.models import Student
from teachers.models import Teacher
from courses.models import Course, Enrollment
from attendance.models import Attendance


@login_required
def dashboard(request):
    user = request.user
    if user.is_superuser or user.role == 'admin':
        return _admin_dashboard(request)
    elif user.role == 'teacher':
        return _teacher_dashboard(request)
    else:
        return _student_dashboard(request)


def _admin_dashboard(request):
    total_students = Student.objects.count()
    total_teachers = Teacher.objects.count()
    total_courses = Course.objects.filter(is_active=True).count()
    total_enrollments = Enrollment.objects.filter(status='active').count()

    total_attendance = Attendance.objects.count()
    present_count = Attendance.objects.filter(status=Attendance.Status.PRESENT).count()
    attendance_rate = round((present_count / total_attendance * 100), 2) if total_attendance > 0 else 0

    recent_students = Student.objects.order_by('-enrollment_date')[:5]

    context = {
        'dashboard_type': 'admin',
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_courses': total_courses,
        'total_enrollments': total_enrollments,
        'attendance_rate': attendance_rate,
        'recent_students': recent_students,
    }
    return render(request, 'dashboard.html', context)


def _teacher_dashboard(request):
    teacher = request.user.teacher_profile
    courses = teacher.courses.filter(is_active=True)
    enrolled_students = sum(c.enrolled_students_count for c in courses)

    course_ids = courses.values_list('id', flat=True)
    total_attendance = Attendance.objects.filter(course_id__in=course_ids).count()
    present_count = Attendance.objects.filter(
        course_id__in=course_ids, status=Attendance.Status.PRESENT
    ).count()
    attendance_rate = round((present_count / total_attendance * 100), 2) if total_attendance > 0 else 0

    from grades.models import Mark
    percentage_expr = ExpressionWrapper(
        F('marks_obtained') / F('max_marks') * 100,
        output_field=DecimalField(max_digits=5, decimal_places=2)
    )
    avg_score = Mark.objects.filter(course_id__in=course_ids).aggregate(overall_avg=Avg(percentage_expr))
    avg_score = round(avg_score['overall_avg'], 2) if avg_score['overall_avg'] is not None else 0

    context = {
        'dashboard_type': 'teacher',
        'teacher': teacher,
        'courses': courses,
        'enrolled_students': enrolled_students,
        'attendance_rate': attendance_rate,
        'avg_score': avg_score,
        'total_marks_entered': Mark.objects.filter(course_id__in=course_ids).count(),
    }
    return render(request, 'dashboard.html', context)


def _student_dashboard(request):
    student = request.user.student_profile
    courses = student.get_enrolled_courses()
    attendance_rate = student.get_attendance_percentage()
    avg_marks = student.get_average_marks()

    from grades.models import Mark
    recent_marks = Mark.objects.filter(student=student).order_by('-exam_date')[:5]

    context = {
        'dashboard_type': 'student',
        'student': student,
        'courses': courses,
        'attendance_rate': attendance_rate,
        'avg_marks': avg_marks,
        'recent_marks': recent_marks,
    }
    return render(request, 'dashboard.html', context)
