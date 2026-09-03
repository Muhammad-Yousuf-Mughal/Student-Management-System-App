from django.db import models


class Attendance(models.Model):
    class Status(models.TextChoices):
        PRESENT = 'present', 'Present'
        ABSENT = 'absent', 'Absent'
        LATE = 'late', 'Late'

    student = models.ForeignKey(
        'students.Student', on_delete=models.CASCADE, related_name='attendances'
    )
    course = models.ForeignKey(
        'courses.Course', on_delete=models.CASCADE, related_name='attendances'
    )
    date = models.DateField()
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PRESENT)
    remarks = models.CharField(max_length=200, blank=True)

    class Meta:
        unique_together = ('student', 'course', 'date')
        ordering = ['-date', 'student']
        verbose_name = 'Attendance'
        verbose_name_plural = 'Attendances'

    def __str__(self):
        return f'{self.student} - {self.course} - {self.date} - {self.status}'
