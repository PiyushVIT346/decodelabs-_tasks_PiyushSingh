"""
storage.py
----------
All persistence concerns for the app live here: user accounts, and the
introspection/ledger helpers that power the "Storage Inspector" panel in
the frontend. Keeping this separate from app.py and chain.py means the
web layer never touches sqlite3 directly.
"""

import os
import sqlite3
from datetime import datetime, timezone

from werkzeug.security import check_password_hash, generate_password_hash

DB_FILE = os.path.join(os.path.dirname(__file__), "app_data.db")

# Tables LangChain's SQLChatMessageHistory creates on demand. We only need
# the name to report row counts; LangChain manages its own schema.
LC_HISTORY_TABLE = "message_store"
LEDGER_TABLE = "storage_ledger"


def get_connection() -> sqlite3.Connection:
    """Single place that opens a connection, so pragmas stay consistent."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Create the users table and the storage_ledger audit table."""
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {LEDGER_TABLE} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ts TEXT NOT NULL,
                username TEXT,
                event TEXT NOT NULL,
                detail TEXT
            )
            """
        )
        conn.commit()


# --------------------------------------------------------------------------
# Users
# --------------------------------------------------------------------------

def create_user(username: str, password: str) -> bool:
    """Insert a new user with a hashed password. Returns False if taken."""
    username = username.strip().lower()
    if not username or not password:
        return False
    with get_connection() as conn:
        try:
            conn.execute(
                "INSERT INTO users (username, password_hash, created_at) VALUES (?, ?, ?)",
                (username, generate_password_hash(password), _now()),
            )
            conn.commit()
        except sqlite3.IntegrityError:
            return False
    append_ledger("user_registered", username=username)
    return True


def verify_user(username: str, password: str) -> bool:
    """Check credentials against the stored hash (never plaintext)."""
    username = username.strip().lower()
    with get_connection() as conn:
        row = conn.execute(
            "SELECT password_hash FROM users WHERE username = ?", (username,)
        ).fetchone()
    ok = bool(row) and check_password_hash(row["password_hash"], password)
    append_ledger("login_success" if ok else "login_failed", username=username)
    return ok


# --------------------------------------------------------------------------
# Ledger (a real, persisted log of storage events - not just in-memory)
# --------------------------------------------------------------------------

def append_ledger(event: str, username: str | None = None, detail: str = "") -> None:
    """Write one row to storage_ledger. Every register/login/message hits this."""
    with get_connection() as conn:
        conn.execute(
            f"INSERT INTO {LEDGER_TABLE} (ts, username, event, detail) VALUES (?, ?, ?, ?)",
            (_now(), username, event, detail),
        )
        conn.commit()


def recent_ledger(limit: int = 25) -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute(
            f"SELECT ts, username, event, detail FROM {LEDGER_TABLE} "
            f"ORDER BY id DESC LIMIT ?",
            (limit,),
        ).fetchall()
    return [dict(r) for r in rows]


# --------------------------------------------------------------------------
# Storage stats (what powers the inspector panel)
# --------------------------------------------------------------------------

def get_db_stats() -> dict:
    """Report file size and per-table row counts for the whole SQLite file."""
    size_bytes = os.path.getsize(DB_FILE) if os.path.exists(DB_FILE) else 0

    with get_connection() as conn:
        table_names = [
            r["name"]
            for r in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
            ).fetchall()
        ]
        tables = []
        for name in table_names:
            count = conn.execute(f"SELECT COUNT(*) AS c FROM {name}").fetchone()["c"]
            tables.append({"name": name, "rows": count})

    return {
        "db_file": os.path.basename(DB_FILE),
        "size_bytes": size_bytes,
        "size_human": _human_size(size_bytes),
        "tables": sorted(tables, key=lambda t: t["name"]),
    }


def get_session_message_count(session_id: str) -> int:
    """Row count for a single user's slice of message_store, if it exists."""
    with get_connection() as conn:
        exists = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name = ?",
            (LC_HISTORY_TABLE,),
        ).fetchone()
        if not exists:
            return 0
        row = conn.execute(
            f"SELECT COUNT(*) AS c FROM {LC_HISTORY_TABLE} WHERE session_id = ?",
            (session_id,),
        ).fetchone()
        return row["c"]


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%H:%M:%S")


def _human_size(n: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024:
            return f"{n:.0f} {unit}" if unit == "B" else f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} TB"