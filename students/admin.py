from django.contrib import admin
from students.models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'full_name', 'grade_level', 'enrollment_date', 'user_email')
    list_filter = ('grade_level', 'enrollment_date')
    search_fields = ('student_id', 'user__first_name', 'user__last_name', 'user__email')
    readonly_fields = ('enrollment_date',)

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'Email'
