"""
Sample data management command for the Student Management System.
Usage: python manage.py seed_data
"""
import random
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from django.db import transaction

from accounts.models import User
from students.models import Student
from teachers.models import Teacher
from courses.models import Department, Course, Enrollment
from attendance.models import Attendance
from grades.models import Mark


class Command(BaseCommand):
    help = 'Seed sample data for the Student Management System'

    def add_arguments(self, parser):
        parser.add_argument('--reset', action='store_true', help='Delete all existing data first')

    @transaction.atomic
    def handle(self, *args, **options):
        if options.get('reset'):
            self.stdout.write('Deleting existing data...')
            Mark.objects.all().delete()
            Attendance.objects.all().delete()
            Enrollment.objects.all().delete()
            Course.objects.all().delete()
            Department.objects.all().delete()
            Student.objects.all().delete()
            Teacher.objects.all().delete()
            User.objects.filter(is_superuser=False).delete()

        self.stdout.write('Creating sample data...')

        # Create admin
        admin, _ = User.objects.get_or_create(
            email='admin@school.com',
            defaults={'first_name': 'System', 'last_name': 'Admin', 'role': User.Role.ADMIN, 'is_staff': True, 'is_superuser': True}
        )
        admin.set_password('admin123')
        admin.save()
        self.stdout.write(self.style.SUCCESS(f'Admin: admin@school.com / admin123'))

        # Create departments
        dept_cs, _ = Department.objects.get_or_create(
            name='Computer Science', code='CS',
            defaults={'description': 'Department of Computer Science'}
        )
        dept_math, _ = Department.objects.get_or_create(
            name='Mathematics', code='MATH',
            defaults={'description': 'Department of Mathematics'}
        )
        dept_eng, _ = Department.objects.get_or_create(
            name='English Literature', code='ENG',
            defaults={'description': 'Department of English Literature'}
        )

        # Create teachers
        teacher_data = [
            ('John', 'Smith', 'EMP001', 'Computer Science', 'M.Sc. Computer Science', date(2020, 1, 15)),
            ('Sarah', 'Johnson', 'EMP002', 'Mathematics', 'M.Sc. Mathematics', date(2019, 8, 10)),
            ('Michael', 'Brown', 'EMP003', 'English Literature', 'M.A. English', date(2021, 3, 1)),
            ('Emily', 'Davis', 'EMP004', 'Computer Science', 'Ph.D. Computer Science', date(2018, 6, 20)),
        ]
        teachers = []
        for first, last, emp_id, dept, qual, hire_date in teacher_data:
            email = f'{first.lower()}.{last.lower()}@school.com'
            user, _ = User.objects.get_or_create(
                email=email,
                defaults={'first_name': first, 'last_name': last, 'role': User.Role.TEACHER, 'is_active': True}
            )
            user.set_password('teacher123')
            user.save()
            teacher, _ = Teacher.objects.get_or_create(
                user=user,
                defaults={'employee_id': emp_id, 'department': dept, 'qualification': qual, 'hire_date': hire_date}
            )
            teachers.append(teacher)
        self.stdout.write(self.style.SUCCESS(f'Created {len(teachers)} teachers (password: teacher123)'))

        # Create students
        student_names = [
            ('Alice', 'Williams', 'STU001', 'Grade 10', 'Robert Williams', '555-0101'),
            ('Bob', 'Jones', 'STU002', 'Grade 10', 'Mary Jones', '555-0102'),
            ('Charlie', 'Garcia', 'STU003', 'Grade 10', 'Maria Garcia', '555-0103'),
            ('Diana', 'Miller', 'STU004', 'Grade 11', 'James Miller', '555-0104'),
            ('Ethan', 'Davis', 'STU005', 'Grade 11', 'Susan Davis', '555-0105'),
            ('Fiona', 'Rodriguez', 'STU006', 'Grade 11', 'Carlos Rodriguez', '555-0106'),
            ('George', 'Martinez', 'STU007', 'Grade 12', 'Linda Martinez', '555-0107'),
            ('Hannah', 'Hernandez', 'STU008', 'Grade 12', 'Joseph Hernandez', '555-0108'),
            ('Ian', 'Lopez', 'STU009', 'Grade 12', 'Patricia Lopez', '555-0109'),
            ('Julia', 'Wilson', 'STU010', 'Grade 10', 'John Wilson', '555-0110'),
        ]
        students = []
        for first, last, sid, grade, parent, phone in student_names:
            email = f'{first.lower()}.{last.lower()}@student.com'
            user, _ = User.objects.get_or_create(
                email=email,
                defaults={'first_name': first, 'last_name': last, 'role': User.Role.STUDENT, 'is_active': True}
            )
            user.set_password('student123')
            user.save()
            student, _ = Student.objects.get_or_create(
                user=user,
                defaults={
                    'student_id': sid, 'grade_level': grade, 'parent_guardian': parent,
                    'parent_phone': phone, 'date_of_birth': date(2008, random.randint(1, 12), random.randint(1, 28))
                }
            )
            students.append(student)
        self.stdout.write(self.style.SUCCESS(f'Created {len(students)} students (password: student123)'))

        # Create courses
        course_data = [
            ('CS101', 'Introduction to Programming', 'Learn programming basics', 3, dept_cs, teachers[0]),
            ('CS201', 'Data Structures and Algorithms', 'Advanced data structures', 4, dept_cs, teachers[3]),
            ('MATH101', 'Calculus I', 'Limits, derivatives, integrals', 4, dept_math, teachers[1]),
            ('MATH201', 'Linear Algebra', 'Vectors and matrices', 3, dept_math, teachers[1]),
            ('ENG101', 'English Composition', 'Writing skills', 3, dept_eng, teachers[2]),
            ('ENG201', 'World Literature', 'Classic literature', 3, dept_eng, teachers[2]),
        ]
        courses = []
        for code, name, desc, credits, dept, teacher in course_data:
            course, _ = Course.objects.get_or_create(
                course_code=code,
                defaults={'name': name, 'description': desc, 'credits': credits, 'department': dept, 'teacher': teacher, 'is_active': True}
            )
            courses.append(course)
        self.stdout.write(self.style.SUCCESS(f'Created {len(courses)} courses'))

        # Set department head
        dept_cs.head = teachers[3]
        dept_cs.save()
        dept_math.head = teachers[1]
        dept_math.save()
        dept_eng.head = teachers[2]
        dept_eng.save()

        # Enroll students in courses
        for student in students:
            for course in random.sample(courses, k=random.randint(3, 5)):
                Enrollment.objects.get_or_create(student=student, course=course)

        # Create attendance records
        statuses = [Attendance.Status.PRESENT] * 8 + [Attendance.Status.ABSENT, Attendance.Status.LATE]
        for student in students:
            for course in student.courses.all():
                for days_ago in range(1, 30):
                    att_date = date.today() - timedelta(days=days_ago)
                    Attendance.objects.get_or_create(
                        student=student, course=course, date=att_date,
                        defaults={'status': random.choice(statuses)}
                    )

        # Create marks
        exam_types = ['midterm', 'final', 'quiz', 'assignment']
        for student in students:
            for course in student.courses.all():
                for exam_type in random.sample(exam_types, k=random.randint(2, 3)):
                    max_marks = 100
                    obtained = random.randint(40, 95)
                    Mark.objects.get_or_create(
                        student=student, course=course, exam_type=exam_type,
                        defaults={
                            'marks_obtained': obtained, 'max_marks': max_marks,
                            'exam_date': date.today() - timedelta(days=random.randint(1, 60))
                        }
                    )

        self.stdout.write(self.style.SUCCESS('Sample data created successfully!'))
        self.stdout.write('')
        self.stdout.write('Login credentials:')
        self.stdout.write('  Admin:   admin@school.com / admin123')
        self.stdout.write('  Teacher: john.smith@school.com / teacher123')
        self.stdout.write('  Student: alice.williams@student.com / student123')
