import sqlite3

def create_database():
    conn = sqlite3.connect("hotel.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            phone TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rooms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_no INTEGER,
            room_type TEXT,
            price REAL,
            status TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer TEXT,
            room_no INTEGER,
            checkin TEXT,
            checkout TEXT,
            status TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer TEXT,
            amount REAL,
            method TEXT,
            status TEXT
        )
    """)

    conn.commit()
    conn.close()

    print("Database created successfully!")

if __name__ == "__main__":
    create_database()