import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect("tracker.db")
    cursor = conn.cursor()
    # Atomic Tracking Ledger
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS exercise_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            log_date DATE NOT NULL,
            exercise_name TEXT NOT NULL,
            set_number INTEGER NOT NULL,
            reps INTEGER NOT NULL,
            weight REAL NOT NULL,
            duration_seconds INTEGER NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # Persistent Day-Wise Templates
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS routine_templates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            day_name TEXT NOT NULL,
            exercise_name TEXT NOT NULL,
            target_sets INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def log_session(date: str, exercise: str, set_no: int, reps: int, weight: float, duration: int):
    conn = sqlite3.connect("tracker.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO exercise_logs (log_date, exercise_name, set_number, reps, weight, duration_seconds) 
        VALUES (?, ?, ?, ?, ?, ?)
    """, (date, exercise, set_no, reps, weight, duration))
    conn.commit()
    conn.close()

def save_template(day_name: str, exercises: list):
    conn = sqlite3.connect("tracker.db")
    cursor = conn.cursor()
    # Purge old template for this day to maintain a single source of truth
    cursor.execute("DELETE FROM routine_templates WHERE day_name = ?", (day_name,))
    for ex in exercises:
        cursor.execute("""
            INSERT INTO routine_templates (day_name, exercise_name, target_sets) 
            VALUES (?, ?, ?)
        """, (day_name, ex['name'], ex['targetSets']))
    conn.commit()
    conn.close()

def get_template(day_name: str):
    conn = sqlite3.connect("tracker.db")
    cursor = conn.cursor()
    cursor.execute("SELECT exercise_name, target_sets FROM routine_templates WHERE day_name = ? ORDER BY id ASC", (day_name,))
    rows = cursor.fetchall()
    conn.close()
    return [{"name": r[0], "targetSets": r[1]} for r in rows]