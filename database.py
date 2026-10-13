
import sqlite3
from pathlib import Path
from datetime import date

DATABASE_PATH = Path(__file__).resolve().parent / "hotels.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS hotels (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                location TEXT NOT NULL,
                price REAL NOT NULL CHECK(price > 0),
                rating REAL NOT NULL DEFAULT 4.0,
                image_url TEXT,
                description TEXT NOT NULL,
                amenities TEXT NOT NULL DEFAULT 'Wi-Fi, AC'
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                guest_name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL,
                hotel_id INTEGER NOT NULL,
                check_in TEXT NOT NULL,
                check_out TEXT NOT NULL,
                guests INTEGER NOT NULL CHECK(guests > 0),
                rooms INTEGER NOT NULL CHECK(rooms > 0),
                total_price REAL NOT NULL,
                status TEXT NOT NULL DEFAULT 'Confirmed',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (hotel_id) REFERENCES hotels(id)
            )
        """)

        count = conn.execute(
            "SELECT COUNT(*) FROM hotels"
        ).fetchone()[0]

        if count == 0:
            hotels = [
                (
                    "Grand Palace Hotel", "Mumbai", 3500, 4.5,
                    "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=900",
                    "Enjoy a comfortable stay in the heart of Mumbai.",
                    "Wi-Fi, AC, Restaurant, Room Service"
                ),
                (
                    "Sea View Resort", "Goa", 4200, 4.7,
                    "https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=900",
                    "A relaxing resort for your next beach holiday.",
                    "Wi-Fi, Pool, Beach Access, Restaurant"
                ),
                (
                    "Mountain Retreat", "Manali", 2800, 4.4,
                    "https://images.unsplash.com/photo-1510798831971-661eb04b3739?w=900",
                    "A peaceful mountain stay with beautiful views.",
                    "Wi-Fi, Mountain View, Heating, Restaurant"
                ),
                (
                    "Royal Orchid", "Pune", 3000, 4.3,
                    "https://images.unsplash.com/photo-1564501049412-61c2a3083791?w=900",
                    "Modern rooms for business and leisure travellers.",
                    "Wi-Fi, AC, Gym, Restaurant"
                ),
                (
                    "Lake Paradise", "Udaipur", 5000, 4.8,
                    "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=900",
                    "An elegant getaway near the beautiful lakes.",
                    "Wi-Fi, Pool, Lake View, Restaurant"
                ),
                (
                    "City Comfort Inn", "Nashik", 1800, 4.1,
                    "https://images.unsplash.com/photo-1445019980597-93fa8acb246c?w=900",
                    "An affordable and comfortable city stay.",
                    "Wi-Fi, AC, Parking, Breakfast"
                ),
            ]

            conn.executemany("""
                INSERT INTO hotels
                (name, location, price, rating, image_url, description, amenities)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, hotels)


def get_hotels(search=""):
    with get_connection() as conn:
        if search:
            pattern = f"%{search}%"
            rows = conn.execute("""
                SELECT * FROM hotels
                WHERE name LIKE ? OR location LIKE ?
                ORDER BY rating DESC
            """, (pattern, pattern)).fetchall()
        else:
            rows = conn.execute("""
                SELECT * FROM hotels ORDER BY rating DESC
            """).fetchall()

        return [dict(row) for row in rows]



def get_hotel(hotel_id):
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM hotels WHERE id = ?", (hotel_id,)
        ).fetchone()

        if not row:
            return None

        hotel = dict(row)

        # Support databases created by older versions of the project.
        if "amenities" not in hotel:
            hotel["amenities"] = "Wi-Fi, AC, Restaurant"

        return hotel



def create_booking(data):
    with get_connection() as conn:
        cursor = conn.execute("""
            INSERT INTO bookings (
                guest_name, email, phone, hotel_id,
                check_in, check_out, guests, rooms, total_price
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data["guest_name"], data["email"], data["phone"],
            data["hotel_id"], data["check_in"], data["check_out"],
            data["guests"], data["rooms"], data["total_price"]
        ))
        return cursor.lastrowid


def get_booking(booking_id):
    with get_connection() as conn:
        row = conn.execute("""
            SELECT b.*, h.name AS hotel_name, h.location, h.image_url
            FROM bookings b
            JOIN hotels h ON h.id = b.hotel_id
            WHERE b.id = ?
        """, (booking_id,)).fetchone()
        return dict(row) if row else None


def get_all_bookings():
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT b.*, h.name AS hotel_name, h.location
            FROM bookings b
            JOIN hotels h ON h.id = b.hotel_id
            ORDER BY b.id DESC
        """).fetchall()
        return [dict(row) for row in rows]
