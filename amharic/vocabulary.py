"""
╔══════════════════════════════════════════════════════════════╗
║           M E K U R I A   AI   A S S I S T A N T            ║
║           Amharic Categorized Vocabulary Engine              ║
╚══════════════════════════════════════════════════════════════╝
Categorized Amharic-English vocabulary repository covering Technology,
Programming, Daily Life, Business, Education, Science, Health, and Family.
"""

from typing import Dict, List, Any

VOCABULARY_CATEGORIES: Dict[str, List[Dict[str, str]]] = {
    "technology_programming": [
        {"amharic": "ኮምፒውተር", "phonetic": "kompyutär", "english": "Computer", "example": "ኮምፒውተር ላይ እሰራለሁ። (I work on a computer.)"},
        {"amharic": "ሶፍትዌር", "phonetic": "softwer", "english": "Software", "example": "ይህ ሶፍትዌር ፈጣን ነው። (This software is fast.)"},
        {"amharic": "ዳታቤዝ", "phonetic": "databez", "english": "Database", "example": "መረጃው በዳታቤዝ ተቀምጧል። (The data is stored in the database.)"},
        {"amharic": "ኢንተርኔት", "phonetic": "intärnet", "english": "Internet", "example": "የኢንተርኔት ግንኙነት አለኝ። (I have an internet connection.)"},
        {"amharic": "ድህረ-ገጽ", "phonetic": "dəhrä-gäts'", "english": "Website", "example": "አዲስ ድህረ-ገጽ ሰራሁ። (I built a new website.)"},
        {"amharic": "ስህተት / ችግር", "phonetic": "səhtät / chəggər", "english": "Error / Bug", "example": "ኮዱ ውስጥ ስህተት ተገኘ። (A bug was found in the code.)"},
        {"amharic": "ደህንነት", "phonetic": "dähnnät", "english": "Security", "example": "የሲስተሙ ደህንነት የተጠበቀ ነው። (The system security is protected.)"},
        {"amharic": "ማከማቻ / ሜሞሪ", "phonetic": "makämacha / memori", "english": "Memory / Storage", "example": "የማከማቻ ቦታው ሙሉ ነው። (The storage space is full.)"},
    ],
    "daily_conversation": [
        {"amharic": "ሰላም", "phonetic": "sälam", "english": "Hello / Peace", "example": "ሰላም! እንዴት ነህ? (Hello! How are you?)"},
        {"amharic": "እንደምን አደርክ / አደርሽ", "phonetic": "əndämən adärk / adärsh", "english": "Good morning (m/f)", "example": "እንደምን አደርክ ወንድሜ። (Good morning my brother.)"},
        {"amharic": "እንደምን ዋልክ / ዋልሽ", "phonetic": "əndämən walk / walsh", "english": "Good afternoon (m/f)", "example": "እንደምን ዋላችሁ? (Good afternoon everyone.)"},
        {"amharic": "ደህና እደር / እደሪ", "phonetic": "dähna ədär / ədäri", "english": "Good night (m/f)", "example": "ደህና እደሩ። (Good night all.)"},
        {"amharic": "አመሰግናለሁ", "phonetic": "amäsäggənalähu", "english": "Thank you", "example": "በጣም አመሰግናለሁ! (Thank you very much!)"},
        {"amharic": "ይቅርታ", "phonetic": "yəqərta", "english": "Excuse me / Sorry", "example": "ይቅርታ አልሰማሁህም። (Sorry, I didn't hear you.)"},
        {"amharic": "እሺ", "phonetic": "əshi", "english": "Okay / Alright", "example": "እሺ! አሁን አደርገዋለሁ። (Okay! I will do it now.)"},
        {"amharic": "እንኳን ደህና መጣህ / መጣሽ", "phonetic": "ənkwan dähna mät't'ah", "english": "Welcome (m/f)", "example": "ወደ ቤታችን እንኳን ደህና መጣህ። (Welcome to our home.)"},
    ],
    "business_work": [
        {"amharic": "ሥራ", "phonetic": "səra", "english": "Work / Job", "example": "ሥራዬን ጀመርኩ። (I started my work.)"},
        {"amharic": "ስብሰባ", "phonetic": "səbsäba", "english": "Meeting", "example": "ዛሬ ስብሰባ አለን። (We have a meeting today.)"},
        {"amharic": "ቢሮ", "phonetic": "biro", "english": "Office", "example": "ወደ ቢሮ እየሄድኩ ነው። (I am going to the office.)"},
        {"amharic": "ገንዘብ", "phonetic": "gänzäb", "english": "Money", "example": "ገንዘብ አስተላልፌያለሁ። (I have transferred the money.)"},
        {"amharic": "ደንበኛ", "phonetic": "dänbäñña", "english": "Customer / Client", "example": "ደንበኛው ደስተኛ ነው። (The client is happy.)"},
    ],
    "education_school": [
        {"amharic": "ትምህርት ቤት", "phonetic": "təmhərt bet", "english": "School", "example": "ትምህርት ቤት ደረስኩ። (I arrived at school.)"},
        {"amharic": "ተማሪ", "phonetic": "tämari", "english": "Student", "example": "ጎበዝ ተማሪ ነው። (He is a smart student.)"},
        {"amharic": "መምህር", "phonetic": "mämhər", "english": "Teacher", "example": "መምህሩ ትምህርቱን ጀመሩ። (The teacher started the lesson.)"},
        {"amharic": "ፈተና", "phonetic": "fätäna", "english": "Exam / Test", "example": "ፈተናውን አለፍኩ። (I passed the exam.)"},
    ]
}

def get_category_vocabulary(category_key: str) -> List[Dict[str, str]]:
    """Return vocabulary list for a given category."""
    return VOCABULARY_CATEGORIES.get(category_key, VOCABULARY_CATEGORIES["daily_conversation"])

def format_vocabulary_lesson(category_key: str) -> str:
    """Format a structured vocabulary study lesson."""
    words = get_category_vocabulary(category_key)
    cat_title = category_key.replace("_", " ").title()
    lines = [
        f"📚 የቃላት ትምህርት (Vocabulary Lesson): {cat_title}",
        "=" * 50
    ]
    for idx, w in enumerate(words, 1):
        lines.append(f"{idx}. {w['amharic']} ({w['phonetic']}) -> {w['english']}")
        lines.append(f"   ምሳሌ (Example): {w['example']}")
    return "\n".join(lines)
