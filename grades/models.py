from django.db import models


class Mark(models.Model):
    student = models.ForeignKey(
        'students.Student', on_delete=models.CASCADE, related_name='marks'
    )
    course = models.ForeignKey(
        'courses.Course', on_delete=models.CASCADE, related_name='marks'
    )
    exam_type = models.CharField(
        'Exam Type',
        max_length=50,
        choices=[
            ('midterm', 'Midterm'),
            ('final', 'Final'),
            ('quiz', 'Quiz'),
            ('assignment', 'Assignment'),
            ('project', 'Project'),
            ('other', 'Other'),
        ],
        default='final'
    )
    exam_date = models.DateField('Exam Date', blank=True, null=True)
    marks_obtained = models.DecimalField('Marks Obtained', max_digits=5, decimal_places=2)
    max_marks = models.DecimalField('Max Marks', max_digits=5, decimal_places=2, default=100)

    class Meta:
        unique_together = ('student', 'course', 'exam_type')
        ordering = ['-exam_date', 'student']
        verbose_name = 'Mark'
        verbose_name_plural = 'Marks'

    def __str__(self):
        return f'{self.student} - {self.course} - {self.exam_type}: {self.marks_obtained}/{self.max_marks}'

    def get_percentage(self):
        if self.max_marks == 0:
            return 0
        return round((self.marks_obtained / self.max_marks) * 100, 2)

    def calculate_grade(self):
        percentage = self.get_percentage()
        if percentage >= 90:
            return 'A+'
        elif percentage >= 80:
            return 'A'
        elif percentage >= 70:
            return 'B+'
        elif percentage >= 60:
            return 'B'
        elif percentage >= 50:
            return 'C+'
        elif percentage >= 40:
            return 'C'
        elif percentage >= 33:
            return 'D'
        else:
            return 'F'
