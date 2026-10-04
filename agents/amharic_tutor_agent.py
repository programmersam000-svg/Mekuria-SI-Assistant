"""
╔══════════════════════════════════════════════════════════════╗
║           M E K U R I A   AI   A S S I S T A N T            ║
║              Amharic Language & Education Agent              ║
╚══════════════════════════════════════════════════════════════╝
Dedicated specialized agent for Amharic language tutoring,
Fidel lessons, grammar breakdowns, coding explanations in Amharic,
and Ethiopian cultural translation.
"""

from typing import Dict, Any
from agents.base_agent import BaseAgent
import amharic

class AmharicTutorAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="AmharicTutorAgent",
            description="Teaches Amharic (Fidel, vocabulary, grammar, reading), explains coding in Amharic, and provides cultural translation."
        )

    def run(self, goal: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        lower = goal.lower()
        self.log_step("Amharic Intelligence", f"Processing Amharic request: '{goal[:40]}...'")

        # 1. Fidel Lesson
        if "fidel" in lower or "ፊደል" in goal:
            # Pick a root or default to 'ሀ'
            root = "ሀ"
            for r in amharic.list_all_fidel_roots():
                if r in goal:
                    root = r
                    break
            lesson = amharic.get_fidel_lesson(root)
            amharic.amharic_tracker.update_progress(increment_lesson=True)
            return {"type": "fidel_lesson", "content": lesson}

        # 2. Daily Structured Lesson
        elif "lesson" in lower or "ትምህርት" in goal or "አስተምረኝ" in goal:
            lesson = amharic.amharic_teacher.generate_daily_lesson()
            amharic.amharic_tracker.update_progress(increment_lesson=True)
            return {"type": "daily_lesson", "content": lesson}

        # 3. Quiz
        elif "quiz" in lower or "ጥያቄ" in goal or "ፈተና" in goal:
            q = amharic.amharic_teacher.generate_quiz()
            return {"type": "quiz", "content": q}

        # 4. Coding in Amharic
        elif any(k in lower for k in ["variable", "function", "loop", "api", "ኮዲንግ", "ፕሮግራሚንግ"]):
            for concept in ["variable", "function", "loop", "api"]:
                if concept in lower or concept in goal:
                    return {"type": "coding_concept", "content": amharic.explain_coding_concept(concept)}
            return {"type": "coding_concept", "content": amharic.explain_coding_concept("variable")}

        # 5. Idiom & Cultural Expression
        elif any(k in goal for k in ["እጅና ጓንት", "ሆድ ይፍጀው", "ውሃ ቀጠነ", "ፈሊጥ", "idiom"]):
            return {"type": "idiom_explanation", "content": amharic.amharic_translator.explain_idiom(goal)}

        # Default: Daily Lesson
        lesson = amharic.amharic_teacher.generate_daily_lesson()
        return {"type": "daily_lesson", "content": lesson}

amharic_tutor_agent = AmharicTutorAgent()
