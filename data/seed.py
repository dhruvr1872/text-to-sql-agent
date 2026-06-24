"""Seed the sample SQLite database with F1 race data."""
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "sample.db"


def seed() -> None:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.executescript("""
    CREATE TABLE IF NOT EXISTS drivers (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        nationality TEXT,
        team TEXT
    );
    CREATE TABLE IF NOT EXISTS races (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        circuit TEXT,
        year INTEGER,
        winner_id INTEGER REFERENCES drivers(id)
    );
    CREATE TABLE IF NOT EXISTS results (
        id INTEGER PRIMARY KEY,
        race_id INTEGER REFERENCES races(id),
        driver_id INTEGER REFERENCES drivers(id),
        position INTEGER,
        points REAL,
        fastest_lap INTEGER DEFAULT 0
    );
    """)
    c.executemany("INSERT OR IGNORE INTO drivers VALUES (?,?,?,?)", [
        (1, "Max Verstappen", "Dutch", "Red Bull"),
        (2, "Lewis Hamilton", "British", "Mercedes"),
        (3, "Charles Leclerc", "Monegasque", "Ferrari"),
        (4, "Lando Norris", "British", "McLaren"),
        (5, "Carlos Sainz", "Spanish", "Ferrari"),
    ])
    c.executemany("INSERT OR IGNORE INTO races VALUES (?,?,?,?,?)", [
        (1, "Bahrain GP", "Bahrain International Circuit", 2024, 1),
        (2, "Saudi Arabian GP", "Jeddah Corniche Circuit", 2024, 1),
        (3, "Australian GP", "Albert Park Circuit", 2024, 3),
        (4, "Japanese GP", "Suzuka Circuit", 2024, 1),
    ])
    c.executemany("INSERT OR IGNORE INTO results VALUES (?,?,?,?,?,?)", [
        (1,1,1,1,25,1),(2,1,4,2,18,0),(3,1,3,3,15,0),
        (4,2,1,1,25,0),(5,2,2,2,18,1),(6,2,4,3,15,0),
        (7,3,3,1,25,0),(8,3,5,2,18,0),(9,3,4,3,15,1),
        (10,4,1,1,25,1),(11,4,3,2,18,0),(12,4,2,3,15,0),
    ])
    conn.commit()
    conn.close()
    print(f"Seeded {DB_PATH}")


if __name__ == "__main__":
    seed()
