"""
╔══════════════════════════════════════════════════════════════╗
║           M E K U R I A   AI   A S S I S T A N T            ║
║         Automatic Language & Amharic Intent Detector         ║
╚══════════════════════════════════════════════════════════════╝
Detects whether input is English, Amharic, or Mixed, and routes
Amharic assistant commands (error checks, document summaries, timers).
"""

import re
from typing import Tuple, Dict, Any

# Ethiopic Unicode range
ETHIOPIC_REGEX = re.compile(r"[\u1200-\u137F\u1380-\u139F\u2D80-\u2DDF]")

class LanguageDetector:
    """Detects text language and parses Amharic natural intent."""

    @staticmethod
    def detect_language(text: str) -> str:
        """
        Returns:
          - 'amharic' : purely or predominantly Amharic
          - 'mixed'   : contains both English and Amharic
          - 'english' : English / Latin text
        """
        if not text.strip():
            return "english"

        has_ethiopic = bool(ETHIOPIC_REGEX.search(text))
        has_latin = bool(re.search(r"[a-zA-Z]", text))

        if has_ethiopic and has_latin:
            return "mixed"
        elif has_ethiopic:
            return "amharic"
        return "english"

    @staticmethod
    def parse_amharic_intent(text: str) -> Tuple[str | None, str]:
        """
        Identify if an Amharic command maps to a built-in assistant tool.
        Examples:
          - 'ይህን error ፈትሽ' -> ('diagnose', text)
          - 'ሰዓት ስንት ነው' -> ('time', text)
          - 'የኮምፒውተሩን status ንገረኝ' -> ('system_info', text)
          - 'አማርኛ አስተምረኝ' -> ('amharic_lesson', text)
        """
        lower = text.strip()

        if any(k in lower for k in ["ሰዓት", "ቀን", "ዛሬ ምን ቀን ነው"]):
            return "time", text
        elif any(k in lower for k in ["ስርዓት", "ኮምፒውተር", "ሁኔታ", "ራም", "ሜሞሪ", "status"]):
            return "system_info", text
        elif any(k in lower for k in ["አስተምረኝ", "ትምህርት", "ፊደል", "ሰዋሰው", "lesson", "teach"]):
            return "amharic_lesson", text
        elif any(k in lower for k in ["ፈተና", "ጥያቄ", "quiz"]):
            return "amharic_quiz", text
        elif any(k in lower for k in ["ስህተት", "ችግር", "error", "ፈትሽ"]):
            return "diagnose", text
        elif any(k in lower for k in ["አስታውሰኝ", "ቀጠሮ", "alarm", "timer"]):
            return "timer", text
        elif any(k in lower for k in ["ፈልግ", "search", "ድረ-ገጽ", "website"]):
            return "search", text

        return None, text

language_detector = LanguageDetector()
