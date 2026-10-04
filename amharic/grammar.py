"""
╔══════════════════════════════════════════════════════════════╗
║           M E K U R I A   AI   A S S I S T A N T            ║
║                Amharic Grammar & Syntax Engine               ║
╚══════════════════════════════════════════════════════════════╝
Explains Amharic grammar rules: SOV word order, personal pronouns,
verb conjugations (Past, Present/Future), possession suffixes, and negation.
"""

from typing import Dict, Any, List

GRAMMAR_TOPICS: Dict[str, Dict[str, Any]] = {
    "word_order": {
        "title": "የአረፍተ ነገር አወቃቀር (Word Order: SOV)",
        "explanation": (
            "Amharic follows the **SOV (Subject - Object - Verb)** word order, unlike English (SVO).\n"
            "• English: I (Subject) eat (Verb) bread (Object).\n"
            "• Amharic: እኔ (Subject) ዳቦ (Object) እበላለሁ (Verb)."
        ),
        "examples": [
            {"amharic": "ተማሪው መጽሐፍ አነበበ።", "english": "The student read a book.", "breakdown": "ተማሪው (Student) + መጽሐፍ (Book) + አነበበ (Read)"},
            {"amharic": "መኩሪያ ኮምፒውተሩን አስተካከለ።", "english": "Mekuria fixed the computer.", "breakdown": "መኩሪያ (Mekuria) + ኮምፒውተሩን (The Computer) + አስተካከለ (Fixed)"}
        ]
    },
    "personal_pronouns": {
        "title": "መጠሪያ ስሞች (Personal Pronouns)",
        "explanation": "Personal pronouns in Amharic distinguish between male (m), female (f), and polite/formal forms.",
        "examples": [
            {"pronoun": "እኔ (əne)", "english": "I / Me"},
            {"pronoun": "አንተ (antä)", "english": "You (male)"},
            {"pronoun": "አንቺ (anchi)", "english": "You (female)"},
            {"pronoun": "እርስዎ (ərswo)", "english": "You (polite/respectful)"},
            {"pronoun": "እሱ (əssu)", "english": "He / Him"},
            {"pronoun": "እሷ (əsswa)", "english": "She / Her"},
            {"pronoun": "እኛ (əñña)", "english": "We / Us"},
            {"pronoun": "እናንተ (ənnantä)", "english": "You all (plural)"},
            {"pronoun": "እነሱ (ənnässu)", "english": "They / Them"},
        ]
    },
    "possession_suffixes": {
        "title": "የባለቤትነት ቅጥያዎች (Possessive Suffixes)",
        "explanation": "In Amharic, possession is expressed by attaching suffixes directly to the end of nouns.",
        "examples": [
            {"suffix": "-ዬ (-ye)", "meaning": "my", "example": "ቤቴ (My house)"},
            {"suffix": "-ህ (-h)", "meaning": "your (m)", "example": "ቤትህ (Your house - m)"},
            {"suffix": "-ሽ (-sh)", "meaning": "your (f)", "example": "ቤትሽ (Your house - f)"},
            {"suffix": "-ው / -ኡ (-w / -u)", "meaning": "his", "example": "ቤቱ (His house)"},
            {"suffix": "-ዋ (-wa)", "meaning": "her", "example": "ቤትዋ / ቤቷ (Her house)"},
            {"suffix": "-አችን (-achən)", "meaning": "our", "example": "ቤታችን (Our house)"},
        ]
    },
    "negation": {
        "title": "አሉታዊ አረፍተ ነገር (Negation: አል...ም)",
        "explanation": "To negate a past-tense verb in Amharic, wrap the verb with the prefix **አል- (al-)** and the suffix **-ም (-m)**.",
        "examples": [
            {"positive": "ሄደ (He went)", "negative": "አልሄደም (He did not go)"},
            {"positive": "በላሁ (I ate)", "negative": "አልበላሁም (I did not eat)"},
            {"positive": "ሰማ (He heard)", "negative": "አልሰማም (He did not hear)"},
        ]
    }
}

def get_grammar_lesson(topic_key: str) -> str:
    """Generate a structured grammar explanation."""
    topic = GRAMMAR_TOPICS.get(topic_key)
    if not topic:
        return f"የሰዋሰው ርዕስ '{topic_key}' አልተገኘም። እባክዎ ከእነዚህ ይምረጡ: {list(GRAMMAR_TOPICS.keys())}"

    lines = [
        f"📘 የሰዋሰው ትምህርት: {topic['title']}",
        "=" * 50,
        topic["explanation"],
        "\nምሳሌዎች (Examples):"
    ]
    for ex in topic["examples"]:
        if "amharic" in ex:
            lines.append(f"  • {ex['amharic']} -> {ex['english']}  ({ex.get('breakdown', '')})")
        elif "pronoun" in ex:
            lines.append(f"  • {ex['pronoun']} : {ex['english']}")
        elif "positive" in ex:
            lines.append(f"  • {ex['positive']}  --->  {ex['negative']}")
        elif "suffix" in ex:
            lines.append(f"  • {ex['suffix']} ({ex['meaning']}) : {ex['example']}")

    return "\n".join(lines)
