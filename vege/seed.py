from faker import Faker
fake = Faker()
import random
from .models import *
from django.db.models import Sum

def create_subject_marks(n):
    try:
        student_objs = Student.objects.all()
        for student in student_objs:
            subjects = Subject.objects.all()
            for subject in subjects:
                SubjectMarks.objects.create(
                    student=student,
                    subject=subject,
                    marks=random.randint(0, 100)
                )
    except Exception as e:
        print(e)


def seed_db(n=10)-> None:
    try:
        for _ in range(n):
            departments_objs = Department.objects.all()
            random_index = random.randint(0, len(departments_objs) - 1)
            student_id = f'STU-0{random.randint(100, 999)}'
            department = departments_objs[random_index]
            student_name = fake.name()
            student_email = fake.email()
            student_age = random.randint(20, 30)
            student_address = fake.address()

            student_id_obj = StudentID.objects.create(student_id=student_id)

            Student_obj = Student.objects.create(
                department=department,
                student_id=student_id_obj,
                student_name=student_name,
                student_email=student_email,
                student_age=student_age,
                student_address=student_address,
            )
    except Exception as e:
        print(e)



# 22/10/2026: Today I ran few of Advanced Django queries and I found that I can use the above code to get the student with a specific data, get all students name under a department, and get all students with a specific age.

def generate_report_card():
    print('CALLLLLEDD')
    ranks = Student.objects.annotate(marks = Sum('student_marks__marks')).order_by('-marks', 'student_name').all()

    i = 1
    for rank in ranks:
        print(rank)
        ReportCard.objects.create(
            student=rank,
            student_rank=i
        )
        i=i+1