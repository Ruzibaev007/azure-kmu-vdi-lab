import sqlite3

DB = "data/kmu_business.db"

def fetch_all(query, params=()):
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def fetch_one(query, params=()):
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    row = conn.execute(query, params).fetchone()
    conn.close()
    return dict(row) if row else None
