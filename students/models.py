from django.db import models
from django.urls import reverse
from accounts.models import User


class Student(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='student_profile'
    )
    student_id = models.CharField('Student ID', max_length=20, unique=True)
    enrollment_date = models.DateField('Enrollment Date', auto_now_add=True)
    date_of_birth = models.DateField('Date of Birth', blank=True, null=True)
    grade_level = models.CharField('Grade Level', max_length=20, blank=True)
    parent_guardian = models.CharField('Parent/Guardian', max_length=100, blank=True)
    parent_phone = models.CharField('Parent Phone', max_length=20, blank=True)

    class Meta:
        ordering = ['student_id']
        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    def __str__(self):
        return f'{self.user.get_full_name()} ({self.student_id})'

    def get_absolute_url(self):
        return reverse('students:student_detail', kwargs={'pk': self.pk})

    @property
    def full_name(self):
        return self.user.get_full_name() or self.user.email

    def get_enrolled_courses(self):
        return self.enrollments.select_related('course').all()

    def get_average_marks(self):
        from grades.models import Mark
        marks = Mark.objects.filter(student=self)
        if not marks.exists():
            return None
        total = sum(m.marks_obtained for m in marks)
        max_total = sum(m.max_marks for m in marks)
        if max_total == 0:
            return None
        return round((total / max_total) * 100, 2)

    def get_attendance_percentage(self):
        from attendance.models import Attendance
        total = Attendance.objects.filter(student=self).count()
        if total == 0:
            return 0
        present = Attendance.objects.filter(student=self, status=Attendance.Status.PRESENT).count()
        return round((present / total) * 100, 2)
