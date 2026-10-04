CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    branch TEXT,
    cgpa REAL,
    skills TEXT,
    projects TEXT,
    certifications TEXT
);

CREATE TABLE IF NOT EXISTS company_roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_name TEXT NOT NULL,
    role TEXT NOT NULL,
    minimum_cgpa REAL,
    required_skills TEXT,
    package TEXT
);

CREATE TABLE IF NOT EXISTS placements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_name TEXT NOT NULL,
    company_name TEXT NOT NULL,
    role TEXT NOT NULL,
    package TEXT,
    year INTEGER
);

CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT NOT NULL,
    role TEXT NOT NULL
);
