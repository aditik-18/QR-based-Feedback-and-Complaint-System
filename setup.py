import sqlite3
import os

def init_db():
    """Initialize the database with required tables"""
    db_path = "pune_feedback.db"
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create Area table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Area (
            area_id INTEGER PRIMARY KEY AUTOINCREMENT,
            area_name TEXT NOT NULL UNIQUE
        )
    ''')
    
    # Insert default areas
    areas = ["Shivajinagar", "Kothrud", "Hadapsar", "Wakad", "Hinjewadi"]
    for area in areas:
        cursor.execute("INSERT OR IGNORE INTO Area (area_name) VALUES (?)", (area,))
    
    # Create Feedback table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Feedback (
            feedback_id INTEGER PRIMARY KEY AUTOINCREMENT,
            rating INTEGER,
            feedback_text TEXT,
            is_anonymous BOOLEAN,
            area_id INTEGER,
            date TEXT,
            FOREIGN KEY (area_id) REFERENCES Area(area_id)
        )
    ''')
    
    # Create Complaint table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Complaint (
            complaint_id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT,
            phone_number TEXT,
            proof_file TEXT,
            category TEXT,
            status TEXT DEFAULT 'Pending',
            priority_level TEXT,
            area_id INTEGER,
            date TEXT,
            FOREIGN KEY (area_id) REFERENCES Area(area_id)
        )
    ''')
    
    # Create Admin table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Admin (
            admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    ''')
    
    # Insert default admin
    cursor.execute(
        "INSERT OR IGNORE INTO Admin (username, password) VALUES (?, ?)",
        ("admin", "29e710486f5d2a298b242975675321388e1029f54007114b69b313741153401a")
    )
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()