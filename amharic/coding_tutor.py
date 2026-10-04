"""
╔══════════════════════════════════════════════════════════════╗
║           M E K U R I A   AI   A S S I S T A N T            ║
║         Amharic Programming & Computer Science Tutor         ║
╚══════════════════════════════════════════════════════════════╝
Teaches coding concepts (Variables, Functions, Loops, Data Structures,
APIs, Databases, Web Development) in natural Amharic.
"""

from typing import Dict, Any, List

PROGRAMMING_CONCEPTS_AMHARIC: Dict[str, Dict[str, str]] = {
    "variable": {
        "title": "Variable (ተለዋዋጭ መረጃ)",
        "explanation": "Variable ማለት በኮምፒውተር memory ውስጥ መረጃን (ቁጥር፣ ጽሑፍ፣ True/False) ለማስቀመጥ የምንጠቀምበት ስም የተሰጠው ሳጥን ወይም ቦታ ነው።",
        "python_example": "name = 'Mekuria'  # 'Mekuria' የሚለውን ጽሑፍ name በሚባለው variable ውስጥ አስቀመጥነው\nage = 25\nprint(name)",
        "analogy": "እንደ ምልክት የተደረገበት ካርቶን አስበው — ውስጥ እቃ አስቀምጠህ በኋላ በስሙ ታወጣዋለህ።"
    },
    "function": {
        "title": "Function (ተግባር / ፈንክሽን)",
        "explanation": "Function ማለት አንድን የተወሰነ ሥራ የሚሰራ እና በተደጋጋሚ ልንጠራው የምንችለው የኮድ ስብስብ ነው።",
        "python_example": "def say_hello(user_name):\n    return f'ሰላም {user_name}!'\n\nmessage = say_hello('ዮናስ')\nprint(message)  # ሰላም ዮናስ!",
        "analogy": "እንደ ቡና ማፍያ ማሽን — ቡና እና ውሃ ትሰጠዋለህ፣ ተዘጋጅቶ የወጣ ቡና ይሰጥሃል።"
    },
    "loop": {
        "title": "Loop (ድግግሞሽ)",
        "explanation": "Loop ማለት አንድን የኮድ ተግባር በተወሰነ ቁጥር ወይም ሁኔታው እስኪሟላ ድረስ ደጋግሞ የሚያከናውን ነው።",
        "python_example": "for i in range(1, 4):\n    print(f'ትምህርት ቁጥር {i}')",
        "analogy": "እንደ ሰዓት እጅ — 12 እስኪሞላ ድረስ በተደጋጋሚ እንደሚዞረው።"
    },
    "api": {
        "title": "API (Application Programming Interface)",
        "explanation": "API ማለት ሁለት የተለያዩ ሶፍትዌሮች ወይም ድህረ-ገጾች እርስ በእርስ እንዲነጋገሩ እና መረጃ እንዲለዋወጡ የሚያስችል ድልድይ ነው።",
        "python_example": "# API ጥሪ በPython:\nimport requests\nresponse = requests.get('https://api.example.com/weather')\ndata = response.json()",
        "analogy": "በሆቴል ውስጥ እንደ አስተናጋጅ — ትዕዛዝህን ከኩሽና ወስዶ ለአንተ እንደሚያቀርብልህ።"
    }
}

def explain_coding_concept(concept_key: str) -> str:
    """Explain a software engineering concept in Amharic."""
    c = PROGRAMMING_CONCEPTS_AMHARIC.get(concept_key.lower())
    if not c:
        return f"የኮዲንግ ጽንሰ-ሀሳብ '{concept_key}' አልተገኘም። እባክዎ ከእነዚህ ይምረጡ: {list(PROGRAMMING_CONCEPTS_AMHARIC.keys())}"

    lines = [
        f"💻 የኮዲንግ ትምህርት: {c['title']}",
        "=" * 50,
        f"ማብራሪያ (Explanation):\n{c['explanation']}\n",
        f"የህይወት ምሳሌ (Analogy):\n{c['analogy']}\n",
        f"የPython ምሳሌ ኮድ (Example Code):\n```python\n{c['python_example']}\n```"
    ]
    return "\n".join(lines)
