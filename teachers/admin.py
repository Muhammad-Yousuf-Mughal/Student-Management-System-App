from django.contrib import admin
from teachers.models import Teacher


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'full_name', 'department', 'qualification', 'user_email')
    list_filter = ('department',)
    search_fields = ('employee_id', 'user__first_name', 'user__last_name', 'user__email')

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'Email'
