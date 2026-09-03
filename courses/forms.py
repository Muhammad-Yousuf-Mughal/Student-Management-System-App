from django import forms
from courses.models import Course, Department, Enrollment
from accounts.models import User
from teachers.models import Teacher
from students.models import Student


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'code', 'description', 'head']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'head': forms.Select(attrs={'class': 'form-select'}),
        }


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['course_code', 'name', 'description', 'credits', 'department', 'teacher', 'is_active']
        widgets = {
            'course_code': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'credits': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'teacher': forms.Select(attrs={'class': 'form-select'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class EnrollmentForm(forms.ModelForm):
    student = forms.ModelChoiceField(
        queryset=Student.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    course = forms.ModelChoiceField(
        queryset=Course.objects.filter(is_active=True),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    status = forms.ChoiceField(
        choices=[
            ('active', 'Active'),
            ('completed', 'Completed'),
            ('dropped', 'Dropped'),
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    grade = forms.ChoiceField(
        choices=[
            ('A+', 'A+'), ('A', 'A'), ('A-', 'A-'),
            ('B+', 'B+'), ('B', 'B'), ('B-', 'B-'),
            ('C+', 'C+'), ('C', 'C'), ('C-', 'C-'),
            ('D+', 'D+'), ('D', 'D'), ('D-', 'D-'),
            ('F', 'F'), ('', '---------'),
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Enrollment
        fields = ['student', 'course', 'status', 'grade']
