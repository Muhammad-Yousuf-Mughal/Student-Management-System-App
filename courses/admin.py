from django.contrib import admin
from courses.models import Course, Department, Enrollment


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'head', 'courses_count')
    search_fields = ('name', 'code')

    def courses_count(self, obj):
        return obj.courses.count()
    courses_count.short_description = 'Courses'


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_code', 'name', 'department', 'teacher', 'credits', 'is_active')
    list_filter = ('is_active', 'department')
    search_fields = ('course_code', 'name')


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'enrollment_date', 'status', 'grade')
    list_filter = ('status', 'enrollment_date')
    search_fields = ('student__user__first_name', 'student__user__last_name', 'course__name')
