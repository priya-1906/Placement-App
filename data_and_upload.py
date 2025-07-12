
pip install faker;

!pip install mysql-connector-python

from faker import Faker

import random
import pandas as pd
import mysql.connector
from datetime import datetime
from faker import Faker

class DataGenerator:
    def __init__(self, num_students):
        self.num_students = num_students
        self.fake = Faker('en_IN')
        self.years = [2021, 2022, 2023, 2024]
        self.batches = [f"Guvi{year}-{i}" for year in self.years for i in range(1, 6)]

    def generate_email(self, name, domain='gmail.com'):
        username = name.lower().replace(' ', '.').replace(',', '').replace('dr.', '').replace('mr.', '').replace('ms.', '')
        return f"{username}@{domain}"

    def generate_students(self):
        students = []
        for i in range(self.num_students):
            year = random.choice(self.years)
            batch_options = [b for b in self.batches if str(year) in b]
            batch = random.choice(batch_options)

            name = self.fake.name()
            email = self.generate_email(name)

            students.append({
                'name': name,
                'age': random.randint(18, 60),
                'gender': random.choice(['Male', 'Female', 'Other']),
                'email': email,
                'phone': self.fake.phone_number(),
                'enrollment_year': year,
                'course_batch': batch,
                'city': self.fake.city(),
                'graduation_year': year + 1
            })
        return pd.DataFrame(students).astype(object)

    def generate_programming(self, student_ids):
        languages = ['Python', 'SQL', 'Java', 'C++', 'VB', 'C']
        records = []
        programming_id_counter = 1

        for student_id in student_ids:
            num_languages = random.randint(0, 4)
            known_languages = random.sample(languages, num_languages)
            for lang in known_languages:
                records.append({
                    'programming_id': programming_id_counter,
                    'student_id': int(student_id),
                    'language': lang,
                    'problems_solved': random.randint(20, 200),
                    'assessments_completed': random.randint(1, 10),
                    'mini_projects': random.randint(0, 5),
                    'certifications_earned': random.randint(0, 3),
                    'latest_project_score': random.randint(50, 100)
                })
                programming_id_counter += 1

        return pd.DataFrame(records).astype(object)

    def generate_softskills(self, student_ids):
        records = []
        for student_id in student_ids:
            records.append({
                'student_id': int(student_id),
                'communication': random.randint(50, 100),
                'teamwork': random.randint(50, 100),
                'presentation': random.randint(50, 100),
                'leadership': random.randint(50, 100),
                'critical_thinking': random.randint(50, 100),
                'interpersonal_skills': random.randint(50, 100)
            })
        return pd.DataFrame(records).astype(object)

    def generate_placements(self, student_ids):
        statuses = ['Ready', 'Not Ready', 'Placed']
        companies = ['Google', 'Amazon', 'TCS', 'Infosys', 'IBM', 'Accenture']
        records = []
        for student_id in student_ids:
            status = random.choice(statuses)
            company = random.choice(companies) if status == 'Placed' else 'N/A'
            package = random.randint(3, 15) * 100000 if status == 'Placed' else 0
            date = self.fake.date_between(start_date='-2y', end_date='today') if status == 'Placed' else None
            records.append({
                'student_id': int(student_id),
                'mock_interview_score': random.randint(40, 100),
                'internships_completed': random.randint(0, 3),
                'placement_status': status,
                'company_name': company,
                'placement_package': package,
                'interview_rounds_cleared': random.randint(0, 5),
                'placement_date': date.strftime('%Y-%m-%d') if date else None
            })
        return pd.DataFrame(records).astype(object)

import mysql.connector



class DatabaseUploader:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
            user="2VNJytV9sTN2QFc.root",
            password="9RON9MkIJpQMCsbE",
            database="Placement_portal",
            port=4000
        )
        self.cursor = self.conn.cursor()

    def insert_students(self, df):
        query = """
        INSERT INTO Students
        (name, age, gender, email, phone, enrollment_year, course_batch, city, graduation_year)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        student_ids = []
        for _, row in df.iterrows():
            values = (
                str(row['name']), int(row['age']), str(row['gender']), str(row['email']),
                str(row['phone']), int(row['enrollment_year']), str(row['course_batch']),
                str(row['city']), int(row['graduation_year'])
            )
            self.cursor.execute(query, values)
            student_ids.append(self.cursor.lastrowid)
        self.conn.commit()
        return student_ids

    def insert_data(self, df, query, date_columns=None):
        if date_columns is None:
            date_columns = []
        for _, row in df.iterrows():
            values = []
            for col in df.columns:
                val = row[col]
                if col in date_columns and pd.notnull(val):
                    val = datetime.strptime(val, "%Y-%m-%d").date()
                values.append(val)
            self.cursor.execute(query, tuple(values))
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()

generator = DataGenerator(num_students=200)
students_df = generator.generate_students()

uploader = DatabaseUploader()
student_ids = uploader.insert_students(students_df)

programming_df = generator.generate_programming(student_ids)
softskills_df = generator.generate_softskills(student_ids)
placements_df = generator.generate_placements(student_ids)

uploader.insert_data(programming_df, """
INSERT INTO Programming
(programming_id, student_id, language, problems_solved, assessments_completed, mini_projects, certifications_earned,
latest_project_score)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
""")

uploader.insert_data(softskills_df, """
INSERT INTO SoftSkills
(student_id, communication, teamwork, presentation, leadership, critical_thinking, interpersonal_skills)
VALUES (%s, %s, %s, %s, %s, %s, %s)
""")

uploader.insert_data(placements_df, """
INSERT INTO Placements
(student_id, mock_interview_score, internships_completed, placement_status, company_name, placement_package,
interview_rounds_cleared, placement_date)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
""", date_columns=['placement_date'])

uploader.close()
print("Data inserted !")


