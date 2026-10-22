from faker import Faker
fake = Faker()
import random
from .models import *


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