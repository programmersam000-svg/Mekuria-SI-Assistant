"""
╔══════════════════════════════════════════════════════════════╗
║           M E K U R I A   AI   A S S I S T A N T            ║
║         Amharic Language Intelligence & Teaching Subsystem    ║
╚══════════════════════════════════════════════════════════════╝
"""

from amharic.fidel import FIDEL_FAMILIES, get_fidel_lesson, list_all_fidel_roots
from amharic.vocabulary import VOCABULARY_CATEGORIES, format_vocabulary_lesson
from amharic.grammar import GRAMMAR_TOPICS, get_grammar_lesson
from amharic.teacher import amharic_teacher
from amharic.translator import amharic_translator
from amharic.coding_tutor import explain_coding_concept
from amharic.detector import language_detector
from amharic.learning_memory import amharic_tracker

__all__ = [
    "FIDEL_FAMILIES",
    "get_fidel_lesson",
    "list_all_fidel_roots",
    "VOCABULARY_CATEGORIES",
    "format_vocabulary_lesson",
    "GRAMMAR_TOPICS",
    "get_grammar_lesson",
    "amharic_teacher",
    "amharic_translator",
    "explain_coding_concept",
    "language_detector",
    "amharic_tracker",
]
