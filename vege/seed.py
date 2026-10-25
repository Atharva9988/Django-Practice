from faker import Faker
fake = Faker()
import random
import traceback
from datetime import date
from .models import *
from django.db import transaction
from django.db.models import Sum
from django.db.models.functions import Coalesce


def seed_departments_subjects():
    try:
        for d in ['IT', 'Civil', 'Mechanical', 'Electrical', 'Computer Science']:
            Department.objects.get_or_create(department=d)
        for s in ['Maths', 'Physics', 'Chemistry', 'English', 'Programming']:
            Subject.objects.get_or_create(subject_name=s)
        print('Departments and subjects ready')
    except Exception as e:
        traceback.print_exc()


def seed_db(n=10) -> None:
    try:
        departments_objs = list(Department.objects.all())
        if not departments_objs:
            print('No departments found. Run seed_departments_subjects() first.')
            return

        for _ in range(n):
            random_index = random.randint(0, len(departments_objs) - 1)
            department = departments_objs[random_index]
            student_name = fake.name()
            student_age = random.randint(20, 30)
            student_address = fake.address()

            student_id = f'STU-0{random.randint(100, 99999)}'
            while StudentID.objects.filter(student_id=student_id).exists():
                student_id = f'STU-0{random.randint(100, 99999)}'

            student_email = fake.email()
            while Student.admin_objects.filter(student_email=student_email).exists():
                student_email = fake.email()

            with transaction.atomic():
                student_id_obj = StudentID.objects.create(student_id=student_id)

                Student_obj = Student.objects.create(
                    department=department,
                    student_id=student_id_obj,
                    student_name=student_name,
                    student_email=student_email,
                    student_age=student_age,
                    student_address=student_address,
                )
        print(f'Created {n} students')
    except Exception as e:
        traceback.print_exc()


def create_subject_marks(n=None):
    try:
        student_objs = Student.objects.all()
        subjects = Subject.objects.all()
        if not subjects:
            print('No subjects found. Run seed_departments_subjects() first.')
            return

        for student in student_objs:
            for subject in subjects:
                SubjectMarks.objects.get_or_create(
                    student=student,
                    subject=subject,
                    defaults={'marks': random.randint(35, 100)}
                )
        print('Subject marks ready')
    except Exception as e:
        traceback.print_exc()


def generate_report_card():
    try:
        ranks = Student.objects.annotate(
            marks=Coalesce(Sum('subjectmarks__marks'), 0)
        ).order_by('-marks', 'student_name')

        count = 0
        with transaction.atomic():
            ReportCard.objects.filter(
                date_of_report_card_generation=date.today()
            ).delete()

            for rank in ranks:
                count = count + 1
                ReportCard.objects.create(
                    student=rank,
                    student_rank=count
                )
        print(f'Generated {count} report cards')
    except Exception as e:
        traceback.print_exc()


def run_all(n=10):
    seed_departments_subjects()
    seed_db(n)
    create_subject_marks()
    generate_report_card()