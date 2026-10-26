import sqlite3
from pathlib import Path

DB_DIR = Path(__file__).parent / "data"
DB_DIR.mkdir(exist_ok=True)
DB_PATH = DB_DIR / "examsync.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                roll_number TEXT NOT NULL UNIQUE
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS subjects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT NOT NULL UNIQUE,
                name TEXT NOT NULL
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS enrollments (
                student_id INTEGER NOT NULL,
                subject_id INTEGER NOT NULL,
                PRIMARY KEY (student_id, subject_id),
                FOREIGN KEY (student_id) REFERENCES students(id),
                FOREIGN KEY (subject_id) REFERENCES subjects(id)
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS exam_schedule (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject_id INTEGER NOT NULL,
                exam_date TEXT NOT NULL,
                time_slot TEXT NOT NULL,
                FOREIGN KEY (subject_id) REFERENCES subjects(id)
            )
        """)


def add_student(name, roll_number):
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO students (name, roll_number) VALUES (?, ?)",
            (name.strip(), roll_number.strip())
        )


def add_subject(code, name):
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO subjects (code, name) VALUES (?, ?)",
            (code.strip().upper(), name.strip())
        )


def enroll_student(student_id, subject_id):
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO enrollments (student_id, subject_id) VALUES (?, ?)",
            (student_id, subject_id)
        )


def get_students():
    with get_connection() as conn:
        return conn.execute(
            "SELECT id, name, roll_number FROM students ORDER BY roll_number"
        ).fetchall()


def get_subjects():
    with get_connection() as conn:
        return conn.execute(
            "SELECT id, code, name FROM subjects ORDER BY code"
        ).fetchall()


def get_enrollments():
    with get_connection() as conn:
        return conn.execute(
            "SELECT student_id, subject_id FROM enrollments"
        ).fetchall()


def save_schedule(schedule):
    with get_connection() as conn:
        conn.execute("DELETE FROM exam_schedule")
        conn.executemany(
            """
            INSERT INTO exam_schedule (subject_id, exam_date, time_slot)
            VALUES (?, ?, ?)
            """,
            [
                (subject_id, exam_date, time_slot)
                for subject_id, exam_date, time_slot in schedule
            ]
        )


def get_schedule():
    with get_connection() as conn:
        return conn.execute("""
            SELECT s.code, s.name, e.exam_date, e.time_slot
            FROM exam_schedule e
            JOIN subjects s ON s.id = e.subject_id
            ORDER BY e.exam_date, e.time_slot, s.code
        """).fetchall()
