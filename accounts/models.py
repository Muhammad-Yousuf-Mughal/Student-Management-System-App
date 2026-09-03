from django.contrib.auth.models import AbstractUser
from django.db import models
from accounts.managers import UserManager


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'admin', 'Administrator'
        TEACHER = 'teacher', 'Teacher'
        STUDENT = 'student', 'Student'

    ROLE_ADMIN = Role.ADMIN
    ROLE_TEACHER = Role.TEACHER
    ROLE_STUDENT = Role.STUDENT

    username = None
    email = models.EmailField('email address', unique=True)
    role = models.CharField(
        'role',
        max_length=20,
        choices=Role.choices,
        default=Role.STUDENT,
    )
    first_name = models.CharField('first name', max_length=150, blank=True)
    last_name = models.CharField('last name', max_length=150, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'.strip() or self.email

    def get_short_name(self):
        return self.first_name or self.email.split('@')[0]

    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN

    @property
    def is_teacher(self):
        return self.role == self.Role.TEACHER

    @property
    def is_student(self):
        return self.role == self.Role.STUDENT

    def get_role_display_name(self):
        role_map = {
            self.Role.ADMIN: 'Administrator',
            self.Role.TEACHER: 'Teacher',
            self.Role.STUDENT: 'Student',
        }
        return role_map.get(self.role, 'Unknown')
