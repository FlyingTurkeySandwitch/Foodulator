import sqlite3
import os

DB_FILENAME = "MainDB.db"


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "../data", DB_FILENAME)

def get_connection():
    """Returns a connection to the SQLite database."""
    try:
        conn = sqlite3.connect(DB_PATH)
        print(f"DB_manager.py - Opened SQLite database (version {sqlite3.sqlite_version}) successfully.")
        return conn
    except sqlite3.OperationalError as e:
        print("DB_manager.py - Failed to open database:", e)
        return None

def initialize_database(sql_path="DB/initialDB.sql"):
    """(Re)initializes the database from a SQL script."""
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        try:
            with open(sql_path, "r") as f:
                script = f.read()
                cursor.executescript(script)
                conn.commit()
                print("[INFO] Database initialized successfully.")
        except Exception as e:
            print("[ERROR] Failed to initialize DB:", e)
        finally:
            conn.close()
