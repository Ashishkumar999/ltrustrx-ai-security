import sqlite3
import hashlib


# DATABASE CONNECTION

conn = sqlite3.connect("ltrust.db", check_same_thread=False)

conn.row_factory = sqlite3.Row

cursor = conn.cursor()


# USERS TABLE

cursor.execute("""

CREATE TABLE IF NOT EXISTS users (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    username TEXT UNIQUE,

    password TEXT,

    role TEXT DEFAULT 'user'

)

""")

conn.commit()


# SCAN HISTORY TABLE

cursor.execute("""

CREATE TABLE IF NOT EXISTS scan_history (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    username TEXT,

    target TEXT,

    total_issues INTEGER,

    high INTEGER,

    medium INTEGER,

    low INTEGER,

    info INTEGER,

    report_path TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

)

""")

conn.commit()


# HASH PASSWORD

def hash_password(password):

    return hashlib.sha256(password.encode()).hexdigest()


# CREATE USER

def create_user(username, password, role="user"):

    hashed_password = hash_password(password)

    cursor.execute("""

    INSERT INTO users (

        username,
        password,
        role

    )

    VALUES (?, ?, ?)

    """, (

        username,
        hashed_password,
        role

    ))

    conn.commit()


# VALIDATE USER

def validate_user(username, password):

    hashed_password = hash_password(password)

    cursor.execute("""

    SELECT * FROM users

    WHERE username = ?
    AND password = ?

    """, (

        username,
        hashed_password

    ))

    user = cursor.fetchone()

    return user


# SAVE SCAN HISTORY

def save_scan_history(
    username,
    target,
    total_issues,
    high,
    medium,
    low,
    info,
    report_path
):

    cursor.execute("""

    INSERT INTO scan_history (

        username,
        target,
        total_issues,
        high,
        medium,
        low,
        info,
        report_path

    )

    VALUES (?, ?, ?, ?, ?, ?, ?, ?)

    """, (

        username,
        target,
        total_issues,
        high,
        medium,
        low,
        info,
        report_path

    ))

    conn.commit()


# GET SCAN HISTORY

def get_scan_history():

    cursor.execute("""

    SELECT * FROM scan_history

    ORDER BY created_at DESC

    """)

    scans = cursor.fetchall()

    return scans
