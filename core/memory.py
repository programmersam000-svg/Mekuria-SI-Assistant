"""
╔══════════════════════════════════════════════════════════════╗
║           M E K U R I A   AI   A S S I S T A N T            ║
║              Multi-Tier Memory & Knowledge System            ║
╚══════════════════════════════════════════════════════════════╝
Implements:
  1. Working Memory (in-flight goal state, variables, intermediate results)
  2. Short-Term Conversation Memory (recent dialogue turns)
  3. Long-Term Persistent SQLite Memory (User preferences, project history, facts)
  4. Error & Self-Improvement Memory (past bug solutions, successful workflows)
  5. Semantic Knowledge Base (searchable notes, docs, snippets)
"""

import os
import sqlite3
import json
import datetime
from typing import Optional, List, Dict, Any

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
DB_PATH = os.path.join(DATA_DIR, "mekuria_memory.db")

class MemoryManager:
    """Multi-tiered memory subsystem for Mekuria."""
    
    def __init__(self):
        os.makedirs(DATA_DIR, exist_ok=True)
        self._working_memory: Dict[str, Any] = {}
        self._short_term_history: List[Dict[str, str]] = []
        self._init_db()

    def _init_db(self):
        """Initialize SQLite database for persistent long-term storage."""
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            # User preferences and profile facts
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_preferences (
                    key TEXT PRIMARY KEY,
                    value TEXT,
                    updated_at TIMESTAMP
                )
            """)
            # Project metadata and state
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS project_memory (
                    project_name TEXT PRIMARY KEY,
                    details_json TEXT,
                    updated_at TIMESTAMP
                )
            """)
            # Knowledge base (notes, docs, snippets)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS knowledge_base (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    topic TEXT,
                    content TEXT,
                    tags TEXT,
                    created_at TIMESTAMP
                )
            """)
            # Error & Solution learning memory
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS error_solutions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    error_pattern TEXT,
                    root_cause TEXT,
                    solution TEXT,
                    created_at TIMESTAMP
                )
            """)
            conn.commit()

    # ──────────────────────── Working Memory ────────────────────────
    def set_working(self, key: str, value: Any):
        self._working_memory[key] = value

    def get_working(self, key: str, default: Any = None) -> Any:
        return self._working_memory.get(key, default)

    def clear_working(self):
        self._working_memory.clear()

    # ────────────────────── Short-Term Memory ───────────────────────
    def add_turn(self, role: str, content: str):
        self._short_term_history.append({
            "role": role,
            "content": content,
            "time": datetime.datetime.now().isoformat()
        })
        # Keep last 30 messages
        if len(self._short_term_history) > 30:
            self._short_term_history = self._short_term_history[-30:]

    def get_recent_history(self) -> List[Dict[str, str]]:
        return list(self._short_term_history)

    def clear_short_term(self):
        self._short_term_history.clear()

    # ─────────────────────── Long-Term Memory ───────────────────────
    def set_preference(self, key: str, value: str):
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute(
                "INSERT OR REPLACE INTO user_preferences (key, value, updated_at) VALUES (?, ?, ?)",
                (key, value, datetime.datetime.now().isoformat())
            )

    def get_preference(self, key: str, default: str = "") -> str:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT value FROM user_preferences WHERE key = ?", (key,))
            row = cursor.fetchone()
            return row[0] if row else default

    def save_knowledge(self, topic: str, content: str, tags: str = ""):
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute(
                "INSERT INTO knowledge_base (topic, content, tags, created_at) VALUES (?, ?, ?, ?)",
                (topic, content, tags, datetime.datetime.now().isoformat())
            )

    def search_knowledge(self, query: str) -> List[Dict[str, str]]:
        """Search local knowledge base by keyword matching."""
        results = []
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            q = f"%{query}%"
            cursor.execute(
                "SELECT topic, content, tags FROM knowledge_base WHERE topic LIKE ? OR content LIKE ? OR tags LIKE ? LIMIT 5",
                (q, q, q)
            )
            for row in cursor.fetchall():
                results.append({"topic": row[0], "content": row[1], "tags": row[2]})
        return results

    def record_error_solution(self, error_pattern: str, root_cause: str, solution: str):
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute(
                "INSERT INTO error_solutions (error_pattern, root_cause, solution, created_at) VALUES (?, ?, ?, ?)",
                (error_pattern, root_cause, solution, datetime.datetime.now().isoformat())
            )

    def find_learned_solution(self, error_message: str) -> Optional[str]:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT error_pattern, solution FROM error_solutions")
            for pattern, solution in cursor.fetchall():
                if pattern.lower() in error_message.lower():
                    return solution
        return None

# Singleton memory instance
memory = MemoryManager()
