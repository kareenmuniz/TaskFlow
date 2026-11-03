import sqlite3
from pathlib import Path

class TaskRepository:
    def __init__(self, database_path):
        self.database_path = str(database_path)
        Path(self.database_path).parent.mkdir(parents=True, exist_ok=True)
        self.initialize()

    def connect(self):
        connection = sqlite3.connect(self.database_path, timeout=10)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    def initialize(self):
        with self.connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL CHECK(length(trim(title)) BETWEEN 1 AND 120),
                    description TEXT NOT NULL DEFAULT '',
                    priority TEXT NOT NULL CHECK(priority IN ('Baixa','Média','Alta')),
                    due_date TEXT,
                    status TEXT NOT NULL DEFAULT 'Pendente'
                        CHECK(status IN ('Pendente','Concluída')),
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            """)

    def list_all(self, status=None):
        with self.connect() as conn:
            if status in ("Pendente", "Concluída"):
                rows = conn.execute(
                    "SELECT * FROM tasks WHERE status = ? ORDER BY due_date IS NULL, due_date, id DESC",
                    (status,)
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT * FROM tasks ORDER BY due_date IS NULL, due_date, id DESC"
                ).fetchall()
            return [dict(row) for row in rows]

    def get(self, task_id):
        with self.connect() as conn:
            row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
            return dict(row) if row else None

    def insert(self, data):
        with self.connect() as conn:
            cursor = conn.execute("""
                INSERT INTO tasks(title, description, priority, due_date)
                VALUES (?, ?, ?, ?)
            """, (data["title"], data["description"], data["priority"], data["due_date"]))
            return cursor.lastrowid

    def update(self, task_id, data):
        with self.connect() as conn:
            cursor = conn.execute("""
                UPDATE tasks SET title=?, description=?, priority=?, due_date=?
                WHERE id=?
            """, (data["title"], data["description"], data["priority"], data["due_date"], task_id))
            return cursor.rowcount > 0

    def delete(self, task_id):
        with self.connect() as conn:
            cursor = conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            return cursor.rowcount > 0

    def set_status(self, task_id, status):
        with self.connect() as conn:
            cursor = conn.execute("UPDATE tasks SET status=? WHERE id=?", (status, task_id))
            return cursor.rowcount > 0

    def counts(self):
        with self.connect() as conn:
            rows = conn.execute("SELECT status, COUNT(*) total FROM tasks GROUP BY status").fetchall()
            result = {"Pendente": 0, "Concluída": 0}
            result.update({row["status"]: row["total"] for row in rows})
            return result
