from django import forms
from grades.models import Mark


class MarkForm(forms.ModelForm):
    class Meta:
        model = Mark
        fields = ['student', 'course', 'exam_type', 'exam_date', 'marks_obtained', 'max_marks']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-select'}),
            'course': forms.Select(attrs={'class': 'form-select'}),
            'exam_type': forms.Select(attrs={'class': 'form-select'}),
            'exam_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'marks_obtained': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': 0}),
            'max_marks': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': 0}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['course'].disabled = True
