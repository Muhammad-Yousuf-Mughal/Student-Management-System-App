from django import forms
from django.contrib.auth import get_user_model
from students.models import Student

User = get_user_model()


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['student_id', 'date_of_birth', 'grade_level', 'parent_guardian', 'parent_phone']
        widgets = {
            'student_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., STU001'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'grade_level': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Grade 10'}),
            'parent_guardian': forms.TextInput(attrs={'class': 'form-control'}),
            'parent_phone': forms.TextInput(attrs={'class': 'form-control'}),
        }


class StudentRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Student
        fields = ['student_id', 'date_of_birth', 'grade_level', 'parent_guardian', 'parent_phone']
        widgets = {
            'student_id': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'grade_level': forms.TextInput(attrs={'class': 'form-control'}),
            'parent_guardian': forms.TextInput(attrs={'class': 'form-control'}),
            'parent_phone': forms.TextInput(attrs={'class': 'form-control'}),
        }
