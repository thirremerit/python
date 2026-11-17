
import sqlite3
import hashlib
import secrets

DATABASE_NAME = "citycare.db"

ADMIN_USERNAME = "admin"
ADMIN_EMAIL = "admin@citycare.local"
ADMIN_PASSWORD = "citycare123"


# ---------------- DATABASE CONNECTION ----------------

def get_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row
    return connection


# ---------------- PASSWORD SECURITY ----------------

def hash_password(password):
    salt = secrets.token_hex(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt.encode(),
        600000
    ).hex()

    return salt + ":" + password_hash


def verify_password(password, stored_hash):
    salt, original_hash = stored_hash.split(":")

    new_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt.encode(),
        600000
    ).hex()

    return secrets.compare_digest(new_hash, original_hash)


# ---------------- CREATE TABLES ----------------

def create_tables():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            category TEXT NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            status TEXT DEFAULT 'Pending',
            user_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    user_columns = connection.execute(
        "PRAGMA table_info(users)"
    ).fetchall()

    user_column_names = [column["name"] for column in user_columns]

    if "role" not in user_column_names:
        connection.execute("""
            ALTER TABLE users
            ADD COLUMN role TEXT DEFAULT 'citizen'
        """)

    report_columns = connection.execute(
        "PRAGMA table_info(reports)"
    ).fetchall()

    report_column_names = [column["name"] for column in report_columns]

    if "image_path" not in report_column_names:
        connection.execute("""
            ALTER TABLE reports
            ADD COLUMN image_path TEXT
        """)

    # Create administrator if one does not already exist
    admin = connection.execute("""
        SELECT id FROM users WHERE username = ?
    """, (ADMIN_USERNAME,)).fetchone()

    if not admin:
        connection.execute("""
            INSERT INTO users (
                username, email, password_hash, role
            )
            VALUES (?, ?, ?, 'admin')
        """, (
            ADMIN_USERNAME,
            ADMIN_EMAIL,
            hash_password(ADMIN_PASSWORD)
        ))

    connection.commit()
    connection.close()


# ---------------- CREATE CITIZEN ----------------

def create_user(username, email, password):
    connection = get_connection()

    try:
        password_hash = hash_password(password)

        connection.execute("""
            INSERT INTO users (
                username, email, password_hash, role
            )
            VALUES (?, ?, ?, 'citizen')
        """, (username, email, password_hash))

        connection.commit()
        return True, "Account created successfully!"

    except sqlite3.IntegrityError:
        return False, "Username or email already exists."

    finally:
        connection.close()


# ---------------- CREATE GOVERNMENT WORKER ----------------

def create_worker(username, email, password):
    connection = get_connection()

    try:
        password_hash = hash_password(password)

        connection.execute("""
            INSERT INTO users (
                username, email, password_hash, role
            )
            VALUES (?, ?, ?, 'government')
        """, (username, email, password_hash))

        connection.commit()
        return True, "Government worker account created!"

    except sqlite3.IntegrityError:
        return False, "Username or email already exists."

    finally:
        connection.close()


# ---------------- LOGIN USER ----------------

def login_user(identifier, password):
    connection = get_connection()

    user = connection.execute("""
        SELECT * FROM users
        WHERE username = ? COLLATE NOCASE
        OR email = ? COLLATE NOCASE
    """, (identifier, identifier)).fetchone()

    connection.close()

    if user and verify_password(password, user["password_hash"]):
        return {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"],
            "role": user["role"]
        }

    return None


# ---------------- GET GOVERNMENT WORKERS ----------------

def get_workers():
    connection = get_connection()

    workers = connection.execute("""
        SELECT id, username, email
        FROM users
        WHERE role = 'government'
        ORDER BY username
    """).fetchall()

    connection.close()

    return [dict(worker) for worker in workers]


# ---------------- CREATE REPORT ----------------

def create_report(
    title,
    description,
    category,
    latitude,
    longitude,
    user_id,
    image_path=None
):
    connection = get_connection()

    cursor = connection.execute("""
        INSERT INTO reports (
            title,
            description,
            category,
            latitude,
            longitude,
            user_id,
            image_path
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        title,
        description,
        category,
        latitude,
        longitude,
        user_id,
        image_path
    ))

    connection.commit()
    report_id = cursor.lastrowid
    connection.close()

    return report_id


# ---------------- UPDATE REPORT STATUS ----------------

def update_report_status(report_id, new_status):
    allowed_statuses = [
        "Pending",
        "In Progress",
        "Resolved"
    ]

    if new_status not in allowed_statuses:
        return False

    connection = get_connection()

    connection.execute("""
        UPDATE reports
        SET status = ?
        WHERE id = ?
    """, (new_status, report_id))

    connection.commit()
    connection.close()

    return True


# ---------------- GET ALL REPORTS ----------------

def get_all_reports():
    connection = get_connection()

    reports = connection.execute("""
        SELECT
            reports.*,
            users.username AS reported_by
        FROM reports
        LEFT JOIN users
        ON reports.user_id = users.id
        ORDER BY reports.id DESC
    """).fetchall()

    connection.close()

    return [dict(report) for report in reports]


# ---------------- RUN DATABASE ----------------

if __name__ == "__main__":
    create_tables()
    print("CityCare database is ready!")


# ---------------- UPDATE REPORT STATUS ----------------

def update_report_status(report_id, new_status):
    allowed_statuses = [
        "Pending",
        "In Progress",
        "Resolved"
    ]

    if new_status not in allowed_statuses:
        return False

    connection = get_connection()

    connection.execute("""
        UPDATE reports
        SET status = ?
        WHERE id = ?
    """, (new_status, report_id))

    connection.commit()
    connection.close()

    return True