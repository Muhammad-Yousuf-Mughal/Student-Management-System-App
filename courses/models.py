from django.db import models
from accounts.models import User


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True, blank=True)
    description = models.TextField(blank=True)
    head = models.ForeignKey(
        'teachers.Teacher', on_delete=models.SET_NULL, blank=True, null=True,
        related_name='departments_headed'
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'

    def __str__(self):
        return self.name

    def get_courses_count(self):
        return self.courses.count()


class Course(models.Model):
    course_code = models.CharField('Course Code', max_length=20, unique=True)
    name = models.CharField('Course Name', max_length=100)
    description = models.TextField(blank=True)
    credits = models.PositiveIntegerField('Credits', default=3)
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, blank=True, null=True,
        related_name='courses'
    )
    teacher = models.ForeignKey(
        'teachers.Teacher', on_delete=models.SET_NULL, blank=True, null=True,
        related_name='courses'
    )
    students = models.ManyToManyField(
        'students.Student', through='Enrollment', related_name='courses'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['course_code']
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'

    def __str__(self):
        return f'{self.course_code} - {self.name}'

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('courses:course_detail', kwargs={'pk': self.pk})

    @property
    def enrolled_students_count(self):
        return self.students.count()

    def get_students(self):
        return self.students.all()

    def get_teacher(self):
        return self.teacher


class Enrollment(models.Model):
    student = models.ForeignKey(
        'students.Student', on_delete=models.CASCADE, related_name='enrollments'
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='enrollments'
    )
    enrollment_date = models.DateField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('active', 'Active'),
            ('completed', 'Completed'),
            ('dropped', 'Dropped'),
        ],
        default='active'
    )
    grade = models.CharField(max_length=2, blank=True)

    class Meta:
        unique_together = ('student', 'course')
        ordering = ['-enrollment_date']
        verbose_name = 'Enrollment'
        verbose_name_plural = 'Enrollments'

    def __str__(self):
        return f'{self.student} enrolled in {self.course}'

    def get_grade_point(self):
        grade_points = {
            'A+': 4.0, 'A': 4.0, 'A-': 3.7,
            'B+': 3.3, 'B': 3.0, 'B-': 2.7,
            'C+': 2.3, 'C': 2.0, 'C-': 1.7,
            'D+': 1.3, 'D': 1.0, 'D-': 0.7,
            'F': 0.0,
        }
        return grade_points.get(self.grade, None)
