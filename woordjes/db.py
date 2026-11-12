"""SQLite storage for words."""

import os
import sqlite3
from datetime import date
from pathlib import Path

DEFAULT_DB = Path.home() / ".woordjes" / "words.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS words (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    dutch       TEXT NOT NULL UNIQUE,
    english     TEXT NOT NULL,
    box         INTEGER NOT NULL DEFAULT 1,
    due         TEXT NOT NULL,
    times_right INTEGER NOT NULL DEFAULT 0,
    times_wrong INTEGER NOT NULL DEFAULT 0
);
"""


def db_path() -> Path:
    """Database location. Can be changed with the WOORDJES_DB variable."""
    return Path(os.environ.get("WOORDJES_DB", DEFAULT_DB))


def connect(path: Path | None = None) -> sqlite3.Connection:
    path = path or db_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute(SCHEMA)
    return conn


def add_word(conn, dutch: str, english: str, today: date) -> bool:
    """Add a word. Returns False if it already exists."""
    try:
        conn.execute(
            "INSERT INTO words (dutch, english, due) VALUES (?, ?, ?)",
            (dutch.strip(), english.strip(), today.isoformat()),
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False


def all_words(conn):
    return conn.execute("SELECT * FROM words ORDER BY box, dutch").fetchall()


def due_words(conn, today: date, limit: int | None = None):
    sql = "SELECT * FROM words WHERE due <= ? ORDER BY box, due"
    params: tuple = (today.isoformat(),)
    if limit:
        sql += " LIMIT ?"
        params += (limit,)
    return conn.execute(sql, params).fetchall()


def save_answer(conn, word_id: int, box: int, due: date, correct: bool) -> None:
    column = "times_right" if correct else "times_wrong"
    conn.execute(
        f"UPDATE words SET box = ?, due = ?, {column} = {column} + 1 WHERE id = ?",
        (box, due.isoformat(), word_id),
    )
    conn.commit()


def stats(conn, today: date) -> dict:
    total = conn.execute("SELECT COUNT(*) FROM words").fetchone()[0]
    due = conn.execute(
        "SELECT COUNT(*) FROM words WHERE due <= ?", (today.isoformat(),)
    ).fetchone()[0]
    per_box = {
        row["box"]: row["n"]
        for row in conn.execute("SELECT box, COUNT(*) AS n FROM words GROUP BY box")
    }
    return {"total": total, "due": due, "per_box": per_box}
