"""
╔══════════════════════════════════════════════════════════════╗
║           M E K U R I A   AI   A S S I S T A N T            ║
║              Amharic Fidel (ፊደል) Teaching Engine             ║
╚══════════════════════════════════════════════════════════════╝
Complete database of the Ethiopian Fidel script with 7 vowel orders,
phonetic transcriptions, example vocabulary, and interactive practice.
"""

from typing import Dict, Any, List, Optional

# The 7 Vowel Orders in Ge'ez/Amharic
FIDEL_ORDERS = ["ግዕዝ (ä/e)", "ካዕብ (u)", "ሣልስ (i)", "ራብዕ (a)", "ኃምስ (ē)", "ሳድስ (ə/silent)", "ሳብዕ (o)"]

# Primary Fidel Families with Phonetics and Examples
FIDEL_FAMILIES: Dict[str, Dict[str, Any]] = {
    "ሀ": {
        "name": "ሀ (Hoi)",
        "consonant": "h",
        "forms": ["ሀ", "ሁ", "ሂ", "ሃ", "ሄ", "ህ", "ሆ"],
        "phonetics": ["hä", "hu", "hi", "ha", "hē", "h", "ho"],
        "example_words": [
            {"fidel": "ሀብት", "phonetic": "habt", "meaning": "Wealth / Resource"},
            {"fidel": "ሁለት", "phonetic": "hulät", "meaning": "Two"},
            {"fidel": "ሂሳብ", "phonetic": "hisab", "meaning": "Mathematics / Account"},
            {"fidel": "ሃሳብ", "phonetic": "hasab", "meaning": "Idea / Thought"},
            {"fidel": "ሄደ", "phonetic": "hedä", "meaning": "Went"},
            {"fidel": "ህዝብ", "phonetic": "həzb", "meaning": "People / Public"},
            {"fidel": "ሆድ", "phonetic": "hod", "meaning": "Stomach"},
        ]
    },
    "ለ": {
        "name": "ለ (Lawi)",
        "consonant": "l",
        "forms": ["ለ", "ሉ", "ሊ", "ላ", "ሌ", "ል", "ሎ"],
        "phonetics": ["lä", "lu", "li", "la", "lē", "l", "lo"],
        "example_words": [
            {"fidel": "ልጅ", "phonetic": "ləj", "meaning": "Child"},
            {"fidel": "ልብ", "phonetic": "ləb", "meaning": "Heart"},
            {"fidel": "ላም", "phonetic": "lam", "meaning": "Cow"},
            {"fidel": "ሎሚ", "phonetic": "lomi", "meaning": "Lemon"},
        ]
    },
    "መ": {
        "name": "መ (May)",
        "consonant": "m",
        "forms": ["መ", "ሙ", "ሚ", "ማ", "ሜ", "ም", "ሞ"],
        "phonetics": ["mä", "mu", "mi", "ma", "mē", "m", "mo"],
        "example_words": [
            {"fidel": "መጽሐፍ", "phonetic": "mäts'haf", "meaning": "Book"},
            {"fidel": "መምህር", "phonetic": "mämhər", "meaning": "Teacher"},
            {"fidel": "ማታ", "phonetic": "mata", "meaning": "Evening / Night"},
            {"fidel": "ምግብ", "phonetic": "məgb", "meaning": "Food"},
        ]
    },
    "ሠ": {
        "name": "ሠ (Sawt)",
        "consonant": "s",
        "forms": ["ሠ", "ሡ", "ሢ", "ሣ", "ሤ", "ሥ", "ሦ"],
        "phonetics": ["sä", "su", "si", "sa", "sē", "s", "so"],
        "example_words": [
            {"fidel": "ሥራ", "phonetic": "səra", "meaning": "Work / Job"},
            {"fidel": "ሦስት", "phonetic": "sost", "meaning": "Three"},
        ]
    },
    "ረ": {
        "name": "ረ (R'as)",
        "consonant": "r",
        "forms": ["ረ", "ሩ", "ሪ", "ራ", "ሬ", "ር", "ሮ"],
        "phonetics": ["rä", "ru", "ri", "ra", "rē", "r", "ro"],
        "example_words": [
            {"fidel": "ራስ", "phonetic": "ras", "meaning": "Head / Self"},
            {"fidel": "ሩቅ", "phonetic": "ruq", "meaning": "Far"},
            {"fidel": "ሮጠ", "phonetic": "rot'ä", "meaning": "Ran"},
        ]
    },
    "ሰ": {
        "name": "ሰ (Sat)",
        "consonant": "s",
        "forms": ["ሰ", "ሱ", "ሲ", "ሳ", "ሴ", "ስ", "ሶ"],
        "phonetics": ["sä", "su", "si", "sa", "sē", "s", "so"],
        "example_words": [
            {"fidel": "ሰላም", "phonetic": "sälam", "meaning": "Peace / Hello"},
            {"fidel": "ሰው", "phonetic": "säw", "meaning": "Person / Human"},
            {"fidel": "ስም", "phonetic": "səm", "meaning": "Name"},
        ]
    },
    "በ": {
        "name": "በ (Bet)",
        "consonant": "b",
        "forms": ["በ", "ቡ", "ቢ", "ባ", "ቤ", "ብ", "ቦ"],
        "phonetics": ["bä", "bu", "bi", "ba", "bē", "b", "bo"],
        "example_words": [
            {"fidel": "ቤት", "phonetic": "bet", "meaning": "House / Home"},
            {"fidel": "ብርሃን", "phonetic": "bərhan", "meaning": "Light"},
            {"fidel": "በር", "phonetic": "bär", "meaning": "Door / Gate"},
        ]
    },
    "ተ": {
        "name": "ተ (Taw)",
        "consonant": "t",
        "forms": ["ተ", "ቱ", "ቲ", "ታ", "ቴ", "ት", "ቶ"],
        "phonetics": ["tä", "tu", "ti", "ta", "tē", "t", "to"],
        "example_words": [
            {"fidel": "ትምህርት", "phonetic": "təmhərt", "meaning": "Education / Lesson"},
            {"fidel": "ተማሪ", "phonetic": "tämari", "meaning": "Student"},
        ]
    },
    "አ": {
        "name": "አ (Alef)",
        "consonant": "a",
        "forms": ["አ", "ኡ", "ኢ", "ኣ", "ኤ", "እ", "ኦ"],
        "phonetics": ["ä", "u", "i", "a", "ē", "ə", "o"],
        "example_words": [
            {"fidel": "አገር", "phonetic": "agär", "meaning": "Country"},
            {"fidel": "እናት", "phonetic": "ənat", "meaning": "Mother"},
            {"fidel": "አባት", "phonetic": "abbat", "meaning": "Father"},
        ]
    },
    "ከ": {
        "name": "ከ (Kaf)",
        "consonant": "k",
        "forms": ["ከ", "ኩ", "ኪ", "ካ", "ኬ", "ክ", "ኮ"],
        "phonetics": ["kä", "ku", "ki", "ka", "kē", "k", "ko"],
        "example_words": [
            {"fidel": "ከተማ", "phonetic": "kätäma", "meaning": "City"},
            {"fidel": "ኮምፒውተር", "phonetic": "kompyutär", "meaning": "Computer"},
        ]
    },
    "ወ": {
        "name": "ወ (Waw)",
        "consonant": "w",
        "forms": ["ወ", "ዉ", "ዊ", "ዋ", "ዌ", "ው", "ዎ"],
        "phonetics": ["wä", "wu", "wi", "wa", "wē", "w", "wo"],
        "example_words": [
            {"fidel": "ውሃ", "phonetic": "wəha", "meaning": "Water"},
            {"fidel": "ወንድም", "phonetic": "wändəm", "meaning": "Brother"},
        ]
    },
    "የ": {
        "name": "የ (Yaman)",
        "consonant": "y",
        "forms": ["የ", "ዩ", "ዪ", "ያ", "ዬ", "ይ", "ዮ"],
        "phonetics": ["yä", "yu", "yi", "ya", "yē", "y", "yo"],
        "example_words": [
            {"fidel": "የኔ", "phonetic": "yäne", "meaning": "Mine / My"},
            {"fidel": "ዩኒቨርሲቲ", "phonetic": "yunivärsiti", "meaning": "University"},
        ]
    },
    "ደ": {
        "name": "ደ (Dant)",
        "consonant": "d",
        "forms": ["ደ", "ዱ", "ዲ", "ዳ", "ዴ", "ድ", "ዶ"],
        "phonetics": ["dä", "du", "di", "da", "dē", "d", "do"],
        "example_words": [
            {"fidel": "ደስታ", "phonetic": "dästa", "meaning": "Happiness / Joy"},
            {"fidel": "ደብተር", "phonetic": "däbtär", "meaning": "Notebook"},
            {"fidel": "ደህና", "phonetic": "dähna", "meaning": "Fine / Well"},
        ]
    },
    "ገ": {
        "name": "ገ (Gaml)",
        "consonant": "g",
        "forms": ["ገ", "ጉ", "ጊ", "ጋ", "ጌ", "ግ", "ጎ"],
        "phonetics": ["gä", "gu", "gi", "ga", "gē", "g", "go"],
        "example_words": [
            {"fidel": "ገንዘብ", "phonetic": "gänzäb", "meaning": "Money"},
            {"fidel": "ጓደኛ", "phonetic": "gwadäñña", "meaning": "Friend"},
        ]
    },
    "ፈ": {
        "name": "ፈ (Af)",
        "consonant": "f",
        "forms": ["ፈ", "ፉ", "ፊ", "ፋ", "ፌ", "ፍ", "ፎ"],
        "phonetics": ["fä", "fu", "fi", "fa", "fē", "f", "fo"],
        "example_words": [
            {"fidel": "ፍቅር", "phonetic": "fəqr", "meaning": "Love"},
            {"fidel": "ፈጣን", "phonetic": "fät'an", "meaning": "Fast / Quick"},
        ]
    },
    "ፐ": {
        "name": "ፐ (Psa)",
        "consonant": "p",
        "forms": ["ፐ", "ፑ", "ፒ", "ፓ", "ፔ", "ፕ", "ፖ"],
        "phonetics": ["pä", "pu", "pi", "pa", "pē", "p", "po"],
        "example_words": [
            {"fidel": "ፓርክ", "phonetic": "park", "meaning": "Park"},
            {"fidel": "ፖሊስ", "phonetic": "polis", "meaning": "Police"},
        ]
    }
}

def get_fidel_lesson(family_root: str) -> str:
    """Generate a comprehensive lesson for a Fidel family."""
    fam = FIDEL_FAMILIES.get(family_root)
    if not fam:
        return f"ፊደል '{family_root}' በዳታቤዝ ውስጥ አልተገኘም። እባክዎ እንደ 'ሀ', 'ለ', 'መ', 'ሰ', 'በ' ያሉ ፊደላትን ይሞክሩ።"

    lines = [
        f"📖 የፊደል ትምህርት: {fam['name']}",
        "=" * 45,
        f"የፊደል ተከታታይ (7 ቅጾች): {' '.join(fam['forms'])}\n",
        "ቅጾች እና ድምጾች:"
    ]
    for i in range(7):
        lines.append(f"  {i+1}. {fam['forms'][i]} — {fam['phonetics'][i]}  ({FIDEL_ORDERS[i]})")

    lines.append("\nየምሳሌ ቃላት (Example Words):")
    for ex in fam["example_words"]:
        lines.append(f"  • {ex['fidel']} ({ex['phonetic']}) -> {ex['meaning']}")

    lines.append("\nየመጻፍ እና የመለማመጃ ጥያቄ:")
    lines.append(f"  ጥያቄ: የ '{fam['forms'][0]}' አራተኛ ቅጽ (4th order) ምንድነው?")
    lines.append(f"  መልስ: {fam['forms'][3]} ({fam['phonetics'][3]})")

    return "\n".join(lines)

def list_all_fidel_roots() -> List[str]:
    """Return all available Fidel family roots."""
    return list(FIDEL_FAMILIES.keys())
