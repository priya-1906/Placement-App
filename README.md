# Placement Eligibility Streamlit Application

This is a project where i built a Streamlit web application to check which students are eligible for placement based on their activities.


What i Learnt

How to create synthetic data using the **Faker** library.
How to store and manage data using **MySQL database**.
How to write Python code using **Object-Oriented Programming (OOP)**.
How to write **SQL queries** to get useful information.
How to build a **Streamlit dashboard** to display results.


Problem Statement

I want to build a tool where:
- can check student data.
- can filter students based on their scores and skills.
- can see insights like top performers and placement results.


Tables in the Project

1. Students Table
Basic info like name, age, email, city, etc.

2. Programming Table
Details like problems solved, project score, certifications, etc.

3. Soft Skills Table
Communication, teamwork, leadership, etc.

4. Placements Table
Placement status, company name, package, date, etc.


Project Steps

Step 1: Data Generation
I used Faker to generate fake.

Step 2: Database Creation
I created a MySQL database named Placement_portal and created four related tables:

Students
Programming
SoftSkills
Placements

Step 2: Data Upload
I insert this data into MySQL using Python.

Step 3: Streamlit App
I build a simple app to:
- Show all students
- Show top performers
- Search student by name or ID
- Download results

Step 4: SQL Queries
I wrote 10 useful SQL queries to understand the data better.

Outcome

Can filter and see eligible students
View placement reports and scores
Clean code using classes
dashboard


Tools Used

Python
Faker
MySQL
Streamlit
Pandas
