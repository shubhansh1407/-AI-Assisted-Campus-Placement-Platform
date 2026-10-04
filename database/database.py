import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "placement.db")
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "schema.sql")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_database():
    conn = get_connection()
    with open(SCHEMA_PATH, 'r') as f:
        schema = f.read()
    conn.executescript(schema)
    conn.commit()
    conn.close()

def insert_student(name, branch, cgpa, skills, projects, certifications):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO students (name, branch, cgpa, skills, projects, certifications)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (name, branch, cgpa, skills, projects, certifications))
    conn.commit()
    conn.close()

def update_student(name, branch, cgpa, skills, projects, certifications):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE students 
        SET branch = ?, cgpa = ?, skills = ?, projects = ?, certifications = ?
        WHERE name = ?
    ''', (branch, cgpa, skills, projects, certifications, name))
    conn.commit()
    conn.close()

def get_student_by_name(name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM students WHERE name = ?', (name,))
    student = cursor.fetchone()
    conn.close()
    return student

def insert_company_role(company_name, role, minimum_cgpa, required_skills, package):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO company_roles (company_name, role, minimum_cgpa, required_skills, package)
        VALUES (?, ?, ?, ?, ?)
    ''', (company_name, role, minimum_cgpa, required_skills, package))
    conn.commit()
    conn.close()

def insert_placement(student_name, company_name, role, package, year):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO placements (student_name, company_name, role, package, year)
        VALUES (?, ?, ?, ?, ?)
    ''', (student_name, company_name, role, package, year))
    conn.commit()
    conn.close()

def get_students():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT name, branch, cgpa, skills, projects, certifications FROM students')
    students = cursor.fetchall()
    conn.close()
    return [dict(row) for row in students]

def get_company_roles():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT company_name, role, minimum_cgpa, required_skills, package FROM company_roles')
    roles = cursor.fetchall()
    conn.close()
    return [dict(row) for row in roles]

def get_placements():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT student_name, company_name, role, package, year FROM placements')
    placements = cursor.fetchall()
    conn.close()
    return [dict(row) for row in placements]

def get_existing_student_names():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM students')
    names = [row['name'] for row in cursor.fetchall()]
    conn.close()
    return names

def get_company_names():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT company_name FROM company_roles')
    names = [row['company_name'] for row in cursor.fetchall()]
    conn.close()
    return names

def get_roles_by_company(company_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT role FROM company_roles WHERE company_name = ?', (company_name,))
    roles = [row['role'] for row in cursor.fetchall()]
    conn.close()
    return roles
