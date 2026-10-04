"""
╔══════════════════════════════════════════════════════════════╗
║           M E K U R I A   AI   A S S I S T A N T            ║
║        Configuration — voices, persona, and settings         ║
╚══════════════════════════════════════════════════════════════╝
"""

import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

# ──────────────────────────── API Keys ────────────────────────────
GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")

# ──────────────────────────── LLM Settings ────────────────────────
LLM_MODEL: str = "gemini-2.5-flash"           # Fast, intelligent reasoning
LLM_TEMPERATURE: float = 0.7                  # Conversational creativity

# ──────────────────────────── Persona ─────────────────────────────
ASSISTANT_NAME: str = "Mekuria"

SYSTEM_INSTRUCTION: str = (
    f"You are {ASSISTANT_NAME}, an advanced personal AI operating assistant and autonomous digital agent. "
    "You possess first-class bilingual intelligence in both English and Amharic (አማርኛ). "
    "When communicating in Amharic, speak naturally, politely, and fluently with deep cultural fidelity, "
    "understanding Ethiopian idioms, expressions, and technical terminology. "
    "You are capable of teaching Amharic step-by-step (Fidel script, vocabulary, grammar, reading, quizzes) "
    "and explaining programming & technical concepts in clear Amharic. "
    "Keep spoken responses concise, conversational, and direct. "
    "Never use markdown asterisks (*) or raw formatting in spoken voice output. "
    "You have full access to computer tools, research engines, system diagnostics, and autonomous planning."
)

# ──────────────────────────── Voices (TTS) ─────────────────────────
# Popular Edge-TTS Neural Voices:
# English (British): "en-GB-RyanNeural" (default J.A.R.V.I.S. tone), "en-GB-ThomasNeural"
# Amharic:          "am-ET-AmehaNeural" (Male), "am-ET-MekdesNeural" (Female)
# French:           "fr-FR-HenriNeural"
# Spanish:          "es-ES-AlvaroNeural"
TTS_VOICE: str = "en-GB-RyanNeural"
TTS_RATE: str = "+0%"                           # Speed: e.g. "+10%", "-5%"
TTS_VOLUME: str = "+0%"                         # Volume offset
TTS_OUTPUT_FILE: str = "response.mp3"           # Temp audio output file

# ──────────────────────────── Speech-to-Text (STT) ────────────────
WHISPER_MODEL_SIZE: str = "base"                # Options: tiny, base, small, medium, large-v3
WHISPER_DEVICE: str = "cpu"                     # "cpu" or "cuda"
WHISPER_COMPUTE_TYPE: str = "int8"              # int8, float16, float32
STT_LANGUAGE: Optional[str] = None              # None = auto-detect; "en", "am", "fr", etc.

# ──────────────────────────── Audio Recording ─────────────────────
SAMPLE_RATE: int = 16000                        # 16 kHz mono for Whisper
CHANNELS: int = 1
SILENCE_THRESHOLD: float = 0.015                # RMS silence threshold
SILENCE_DURATION: float = 1.5                   # Seconds of silence to end listening
MAX_RECORD_SECONDS: float = 30.0                # Cap on continuous recording

# ──────────────────────────── Wake Word ───────────────────────────
WAKE_WORD_ENABLED: bool = False                 # Set True to enable hands-free wake word
WAKE_WORD_MODEL: str = "hey_jarvis"             # openWakeWord model key
WAKE_WORD_THRESHOLD: float = 0.5                # Confidence score (0-1)

# ──────────────────────────── Memory ──────────────────────────────
AUDIO_TEMP_FILE: str = "temp_recording.wav"
HISTORY_MAX_TURNS: int = 20                     # Maximum turns of conversation memory
