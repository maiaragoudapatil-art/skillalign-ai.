import sqlite3
import pickle

DB_NAME = "data/jobs.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            description TEXT,
            embedding BLOB
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS skill_gaps (
            skill TEXT
        )
    """)

    conn.commit()
    conn.close()

def add_job(title, description, embedding):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    blob = pickle.dumps(embedding)
    cur.execute(
        "INSERT INTO jobs (title, description, embedding) VALUES (?, ?, ?)",
        (title, description, blob),
    )
    conn.commit()
    conn.close()

def get_all_jobs():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT id, title, description, embedding FROM jobs")
    rows = cur.fetchall()
    conn.close()

    jobs = []
    for r in rows:
        emb = pickle.loads(r[3])
        jobs.append((r[0], r[1], r[2], emb))
    return jobs

def log_missing_skills(skills):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    for s in skills:
        cur.execute("INSERT INTO skill_gaps (skill) VALUES (?)", (s,))
    conn.commit()
    conn.close()

def get_skill_gap_stats():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        SELECT skill, COUNT(*)
        FROM skill_gaps
        GROUP BY skill
        ORDER BY COUNT(*) DESC
        LIMIT 10
    """)
    data = cur.fetchall()
    conn.close()
    return data
