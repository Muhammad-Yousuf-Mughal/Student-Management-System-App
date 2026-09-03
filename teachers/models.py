from django.db import models
from accounts.models import User


class Teacher(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='teacher_profile'
    )
    employee_id = models.CharField('Employee ID', max_length=20, unique=True)
    department = models.CharField('Department', max_length=100, blank=True)
    qualification = models.CharField('Qualification', max_length=100, blank=True)
    hire_date = models.DateField('Hire Date', blank=True, null=True)
    phone = models.CharField('Phone', max_length=20, blank=True)

    class Meta:
        ordering = ['employee_id']
        verbose_name = 'Teacher'
        verbose_name_plural = 'Teachers'

    def __str__(self):
        return f'{self.user.get_full_name()} ({self.employee_id})'

    @property
    def full_name(self):
        return self.user.get_full_name() or self.user.email

    def get_assigned_courses(self):
        return self.courses.all()
