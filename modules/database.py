import sqlite3

from passlib.hash import bcrypt


# DATABASE CONNECTION

conn = sqlite3.connect(

    "ltrust.db",

    check_same_thread=False

)

cursor = conn.cursor()


# USERS TABLE

cursor.execute("""

CREATE TABLE IF NOT EXISTS users (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    username TEXT UNIQUE,

    password TEXT

)

""")


# SCAN HISTORY TABLE

cursor.execute("""

CREATE TABLE IF NOT EXISTS scan_history (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    username TEXT,

    target TEXT,

    total INTEGER,

    high INTEGER,

    medium INTEGER,

    low INTEGER,

    info INTEGER,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

)

""")


conn.commit()


# CREATE USER

def create_user(

    username,

    password

):

    hashed_password = bcrypt.hash(password)


    try:

        cursor.execute(

            """

            INSERT INTO users (

                username,

                password

            )

            VALUES (?, ?)

            """,

            (

                username,

                hashed_password

            )

        )


        conn.commit()

        return True


    except:

        return False


# VALIDATE USER

def validate_user(

    username,

    password

):

    cursor.execute(

        """

        SELECT password

        FROM users

        WHERE username=?

        """,

        (username,)

    )


    user = cursor.fetchone()


    if not user:

        return False


    return bcrypt.verify(

        password,

        user[0]

    )


# SAVE SCAN HISTORY

def save_scan_history(

    username,

    target,

    total,

    high,

    medium,

    low,

    info

):

    cursor.execute(

        """

        INSERT INTO scan_history (

            username,

            target,

            total,

            high,

            medium,

            low,

            info

        )

        VALUES (?, ?, ?, ?, ?, ?, ?)

        """,

        (

            username,

            target,

            total,

            high,

            medium,

            low,

            info

        )

    )


    conn.commit()


# GET SCAN HISTORY

def get_scan_history():

    cursor.execute(

        """

        SELECT

            username,

            target,

            total,

            high,

            medium,

            low,

            info,

            created_at

        FROM scan_history

        ORDER BY id DESC

        """

    )


    return cursor.fetchall()
