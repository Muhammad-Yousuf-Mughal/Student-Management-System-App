from django.contrib import admin
from grades.models import Mark


@admin.register(Mark)
class MarkAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'exam_type', 'marks_obtained', 'max_marks', 'get_percentage', 'calculate_grade')
    list_filter = ('exam_type', 'course')
    search_fields = ('student__user__first_name', 'student__user__last_name', 'course__name')
    readonly_fields = ('get_percentage', 'calculate_grade')
