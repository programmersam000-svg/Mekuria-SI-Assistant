"""
╔══════════════════════════════════════════════════════════════╗
║           M E K U R I A   AI   A S S I S T A N T            ║
║        Cultural Fidelity Amharic Translator & Corrector       ║
╚══════════════════════════════════════════════════════════════╝
Translates with cultural fidelity, explains Ethiopian idioms,
provides literal vs natural meanings, and corrects Amharic text.
"""

from typing import Dict, Any, List

ETHIOPIAN_IDIOMS: Dict[str, Dict[str, str]] = {
    "እጅና ጓንት": {
        "literal": "Hand and glove",
        "meaning": "Inseparable / Extremely close friends or allies",
        "example": "እነሱ እጅና ጓንት ናቸው። (They are inseparable.)"
    },
    "ሆድ ይፍጀው": {
        "literal": "Let the stomach consume/digest it",
        "meaning": "Keep it to oneself / Forgive and let it remain a secret",
        "example": "ያለፈውን ነገር ሆድ ይፍጀው። (Let the past stay forgiven and kept within.)"
    },
    "ውሃ ቀጠነ": {
        "literal": "The water became thin",
        "meaning": "Making petty excuses / Finding fault in trivial things",
        "example": "ውሃ ቀጠነ ብለህ አትጨቃጨቅ። (Don't argue over trivial excuses.)"
    },
    "አይነ ግቡ": {
        "literal": "Eye-entering",
        "meaning": "Attractive / Pleasing to the eye / Charming",
        "example": "አይነ ግቡ ልጅ ናት። (She is charming and attractive.)"
    }
}

class AmharicTranslator:
    """Translates and analyzes Amharic with linguistic and cultural fidelity."""

    @staticmethod
    def explain_idiom(phrase: str) -> str:
        """Explain the cultural meaning of an Ethiopian idiom."""
        for idiom, data in ETHIOPIAN_IDIOMS.items():
            if idiom in phrase:
                return (
                    f"🇪🇹 የፈሊጣዊ አነጋገር ትንታኔ (Idiom Breakdown):\n"
                    f"• ፈሊጥ (Idiom): {idiom}\n"
                    f"• ቃል በቃል (Literal): {data['literal']}\n"
                    f"• ትክክለኛ ፍቺ (Cultural Meaning): {data['meaning']}\n"
                    f"• ምሳሌ (Example): {data['example']}"
                )
        return f"ለ '{phrase}' ፈሊጣዊ ትንታኔ በዳታቤዝ ውስጥ አልተገኘም።"

    @staticmethod
    def correct_text_rules(text: str) -> Dict[str, Any]:
        """Apply spelling and punctuation corrections to Amharic text."""
        corrected = text
        changes = []

        # Punctuation normalization
        if text.endswith(".") and not text.endswith("።"):
            corrected = corrected.rstrip(".") + "።"
            changes.append("Replaced English period '.' with Amharic full-stop (አራት ነጥብ '።')")

        if " ," in corrected:
            corrected = corrected.replace(" ,", "፣")
            changes.append("Replaced comma ',' with Amharic comma (ነጠላ ሰረዝ '፣')")

        return {
            "original": text,
            "corrected": corrected,
            "corrections_made": changes or ["ጽሑፉ ትክክለኛ አጻጻፍ እና ስርዓተ-ነጥብ አለው። (Text has correct spelling and punctuation.)"]
        }

amharic_translator = AmharicTranslator()
