"""
╔══════════════════════════════════════════════════════════════╗
║           M E K U R I A   AI   A S S I S T A N T            ║
║              Amharic Teacher & Tutor Subsystem               ║
╚══════════════════════════════════════════════════════════════╝
Implements the full Amharic Teacher Mode:
  - 15-Minute Daily Structured Lessons
  - Graded Reading & Writing Exercises (Beginner -> Advanced)
  - Interactive Multi-Category Quizzes
  - Feedback & Explanation Engine
"""

from typing import Dict, Any, List
import random

from amharic.fidel import FIDEL_FAMILIES, get_fidel_lesson
from amharic.vocabulary import VOCABULARY_CATEGORIES
from amharic.grammar import GRAMMAR_TOPICS, get_grammar_lesson

class AmharicTeacher:
    """Dedicated Amharic tutoring engine for all proficiency levels."""

    def generate_daily_lesson(self, level: str = "Beginner") -> str:
        """Generate a structured 15-minute daily lesson plan."""
        # 1. Fidel of the day
        fidel_root = random.choice(list(FIDEL_FAMILIES.keys()))
        fidel_info = FIDEL_FAMILIES[fidel_root]

        # 2. Daily Vocabulary
        vocab_list = VOCABULARY_CATEGORIES["daily_conversation"][:3]

        # 3. Grammar topic
        grammar_key = random.choice(list(GRAMMAR_TOPICS.keys()))
        grammar_info = GRAMMAR_TOPICS[grammar_key]

        lines = [
            f"🎓 የዕለቱ የ15 ደቂቃ የአማርኛ ትምህርት (Level: {level})",
            "=" * 60,
            f"📌 ክፍል 1: የዕለቱ ፊደል (Fidel of the Day)",
            f"   ፊደል: {' '.join(fidel_info['forms'])} ({fidel_info['consonant']}-family)",
            f"   ምሳሌ: {fidel_info['example_words'][0]['fidel']} ({fidel_info['example_words'][0]['meaning']})\n",
            f"📌 ክፍል 2: አዳዲስ ቃላት (New Vocabulary)",
        ]
        for w in vocab_list:
            lines.append(f"   • {w['amharic']} ({w['phonetic']}) -> {w['english']}")

        lines.extend([
            f"\n📌 ክፍል 3: የሰዋሰው መመሪያ (Grammar Rule)",
            f"   ርዕስ: {grammar_info['title']}",
            f"   {grammar_info['explanation'][:120]}...\n",
            f"📌 ክፍል 4: የንባብ ልምምድ (Reading Exercise)",
            f"   'ሰላም! እኔ መኩሪያ ነኝ። ዛሬ አዲስ ነገር ተምሬያለሁ።'",
            f"   (Hello! I am Mekuria. Today I have learned something new.)\n",
            f"📌 ክፍል 5: የዕለቱ ጥያቄ (Daily Quiz)",
            f"   ጥያቄ: 'Thank you' በአማርኛ ምንድነው?",
            f"   መልስ: አመሰግናለሁ (amäsäggənalähu)"
        ])

        return "\n".join(lines)

    def generate_quiz(self) -> Dict[str, Any]:
        """Generate an interactive multiple-choice quiz question."""
        quizzes = [
            {
                "question": "'Book' በአማርኛ ምን ይባላል?",
                "options": ["A. ቤት", "B. መጽሐፍ", "C. ወንበር", "D. ትምህርት"],
                "answer": "B",
                "explanation": "መጽሐፍ (mäts'haf) means Book. ቤት means House, ወንበር means Chair, and ትምህርት means Education."
            },
            {
                "question": "የ 'ለ' አራተኛ ቅጽ (4th order / ራብዕ) የትኛው ነው?",
                "options": ["A. ሉ", "B. ሊ", "C. ላ", "D. ሌ"],
                "answer": "C",
                "explanation": "ቅጾች: 1.ለ (lä), 2.ሉ (lu), 3.ሊ (li), 4.ላ (la), 5.ሌ (lē), 6.ል (lə), 7.ሎ (lo)."
            },
            {
                "question": "'I am fine' በአማርኛ እንዴት ይገለጻል?",
                "options": ["A. ደህና ነኝ", "B. ሰላም ነኝ", "C. ደህና ሁን", "D. እሺ"],
                "answer": "A",
                "explanation": "ደህና ነኝ (Dähna näñ) means 'I am fine/well'."
            }
        ]
        return random.choice(quizzes)

amharic_teacher = AmharicTeacher()
