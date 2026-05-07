import sqlite3
import bcrypt


DATABASE_NAME = "ltrust.db"


def get_connection():

    conn = sqlite3.connect(DATABASE_NAME)

    conn.row_factory = sqlite3.Row

    return conn


def init_db():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        username TEXT UNIQUE NOT NULL,

        password TEXT NOT NULL,

        role TEXT NOT NULL
    )
    """)

    conn.commit()

    conn.close()


def hash_password(password):

    salt = bcrypt.gensalt()

    hashed = bcrypt.hashpw(
        password.encode(),
        salt
    )

    return hashed.decode()


def verify_password(password, hashed_password):

    return bcrypt.checkpw(
        password.encode(),
        hashed_password.encode()
    )


def create_user(username, password, role="user"):

    conn = get_connection()

    cursor = conn.cursor()

    hashed_password = hash_password(password)

    try:

        cursor.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            (username, hashed_password, role)
        )

        conn.commit()

        return True

    except:

        return False

    finally:

        conn.close()


def validate_user(username, password):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username=?",
        (username,)
    )

    user = cursor.fetchone()

    conn.close()

    if not user:
        return False

    stored_password = user["password"]

    if verify_password(password, stored_password):
        return user

    return False
