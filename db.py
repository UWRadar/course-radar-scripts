import json
import sqlite3

conn = sqlite3.connect("./db.db")
cursor = conn.cursor()

cursor.execute('''
               CREATE TABLE IF NOT EXISTS Courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                courseId TEXT UNIQUE,
                code TEXT,
                subject TEXT,
                value TEXT
               )
               ''')


def insert_course(c, campus: str) -> bool:
    cursor.execute('SELECT courseId FROM Courses WHERE courseId = ?', [c['courseId']])
    existing_course = cursor.fetchone()

    if existing_course:
        # print(f"\nAlready exists: ", {"courseId": c['courseId'], "code": c["code"]})
        return False
    
    try:
        cursor.execute('''
                       INSERT INTO Courses 
                       (courseId, code, subject, campus, value) 
                       VALUES (?, ?, ?, ?, ?)
                       ''', 
                       (c['courseId'], c['code'], c['subject'], campus, json.dumps(c))
                       )
        conn.commit()
        # print("\n[green]Inserted course: ")
        # print({"courseId": c['courseId'], "code": c["code"]})
        return True
    except Exception as e:
        print("\nError occurred while inserting the course:", c['code'])
        print(e)
        return False


def major_exists_in_db(major: str) -> bool:
    cursor.execute('SELECT id, subject FROM Courses WHERE subject = ?', [major])
    existing_course = cursor.fetchone()
    return True if existing_course else False

