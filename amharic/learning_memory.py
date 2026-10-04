"""
╔══════════════════════════════════════════════════════════════╗
║           M E K U R I A   AI   A S S I S T A N T            ║
║              Amharic Learner Progress Tracker                ║
╚══════════════════════════════════════════════════════════════╝
Tracks the user's Amharic proficiency level, completed lessons,
known vocabulary, and spaced repetition review schedule in SQLite.
"""

import sqlite3
import os
import datetime
from typing import Dict, Any, List

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
DB_PATH = os.path.join(DATA_DIR, "mekuria_memory.db")

class AmharicLearningTracker:
    """Manages long-term language learning progress."""

    def __init__(self):
        os.makedirs(DATA_DIR, exist_ok=True)
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS amharic_progress (
                    user_id TEXT PRIMARY KEY,
                    level TEXT,
                    completed_lessons INTEGER,
                    known_words_count INTEGER,
                    last_active TIMESTAMP
                )
            """)
            conn.commit()

    def update_progress(self, level: str = "Beginner", increment_lesson: bool = True):
        """Update student level and lesson count."""
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT completed_lessons, known_words_count FROM amharic_progress WHERE user_id = 'default_user'")
            row = cursor.fetchone()

            if row:
                cur_lessons = row[0] + (1 if increment_lesson else 0)
                cur_words = row[1] + (5 if increment_lesson else 0)
            else:
                cur_lessons = 1 if increment_lesson else 0
                cur_words = 5 if increment_lesson else 0

            cursor.execute("""
                INSERT OR REPLACE INTO amharic_progress (user_id, level, completed_lessons, known_words_count, last_active)
                VALUES ('default_user', ?, ?, ?, ?)
            """, (level, cur_lessons, cur_words, datetime.datetime.now().isoformat()))
            conn.commit()

    def get_progress_report(self) -> str:
        """Return a formatted Amharic learner progress summary."""
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT level, completed_lessons, known_words_count, last_active FROM amharic_progress WHERE user_id = 'default_user'")
            row = cursor.fetchone()

            if not row:
                return "🎓 የአማርኛ ትምህርት ገና አልተጀመረም። 'አማርኛ አስተምረኝ' በማለት ይጀምሩ!"

            return (
                f"📊 የአማርኛ ትምህርት ሂደት (Progress Report):\n"
                f"• ደረጃ (Current Level): {row[0]}\n"
                f"• የተጠናቀቁ ትምህርቶች (Completed Lessons): {row[1]}\n"
                f"• የተማሯቸው ቃላት (Estimated Vocabulary): {row[2]} ቃላት\n"
                f"• የመጨረሻ እንቅስቃሴ: {row[3][:10]}"
            )

amharic_tracker = AmharicLearningTracker()
