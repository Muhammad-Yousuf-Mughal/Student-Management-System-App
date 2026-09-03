from django.contrib import admin
from attendance.models import Attendance


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('date', 'student', 'course', 'status', 'remarks')
    list_filter = ('date', 'status', 'course')
    search_fields = ('student__user__first_name', 'student__user__last_name', 'course__name')
    date_hierarchy = 'date'
