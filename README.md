# 🤖 Mekuria — Your Personal AI Assistant

> *A voice-activated, intelligent AI assistant inspired by J.A.R.V.I.S. — built entirely in Python with free tools and APIs.*

---

## ✨ Features

| Layer | Technology | Description |
|-------|-----------|-------------|
| 🎤 **Hearing** | Faster-Whisper | Local speech-to-text, 99+ languages |
| 🧠 **Thinking** | Google Gemini | LLM reasoning with personality & memory |
| 🔧 **Acting** | Python Tools | Open apps, search web, system controls |
| 🔊 **Speaking** | Edge-TTS | Neural text-to-speech (free British voice) |
| 👂 **Wake Word** | openWakeWord | Optional hands-free activation |

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Your API Key

```bash
# Copy the template and add your Gemini key
cp .env.example .env
```

Get a **free** API key from [Google AI Studio](https://aistudio.google.com/).

### 3. Run Mekuria

```bash
# Text mode (type to chat + voice replies)
python main.py

# Voice mode (speak to chat)
python main.py --voice
```

---

## 📁 Project Structure

```
mekuria/
├── main.py          # 🚀 Entry point — connects all layers
├── config.py        # ⚙️  Configuration (voice, model, persona)
├── brain.py         # 🧠 LLM brain (Gemini + conversation memory)
├── stt.py           # 🎤 Speech-to-Text (Faster-Whisper)
├── tts.py           # 🔊 Text-to-Speech (Edge-TTS)
├── tools.py         # 🔧 Built-in tools & actions
├── wake_word.py     # 👂 Wake word detection (openWakeWord)
├── requirements.txt # 📦 Python dependencies
├── .env.example     # 🔑 API key template
└── README.md        # 📖 This file
```

---

## ⚙️ Configuration

All settings live in [`config.py`](config.py). Key options:

### Change Voice
```python
TTS_VOICE = "en-GB-RyanNeural"      # British male (default)
TTS_VOICE = "en-GB-ThomasNeural"    # Alternative British male
TTS_VOICE = "am-ET-AmehaNeural"     # Amharic male
TTS_VOICE = "fr-FR-HenriNeural"     # French male
```

List all available voices:
```bash
edge-tts --list-voices
```

### Change Language
```python
STT_LANGUAGE = None    # Auto-detect (default)
STT_LANGUAGE = "en"    # English
STT_LANGUAGE = "am"    # Amharic
STT_LANGUAGE = "fr"    # French
STT_LANGUAGE = "ar"    # Arabic
```

### Change Persona
Edit the `SYSTEM_INSTRUCTION` in `config.py` to customize Mekuria's personality and language.

### Enable Wake Word
```python
WAKE_WORD_ENABLED = True
WAKE_WORD_MODEL = "hey_jarvis"
```

---

## 🔧 Built-in Tools

Mekuria can execute these actions:

| Command | Example |
|---------|---------|
| 🕐 **Time** | "What time is it?" |
| 💻 **System Info** | "Give me a system status" |
| 📂 **Open App** | "Open calculator" / "Launch notepad" |
| 🔍 **Web Search** | "Search for Python tutorials" |
| 🌐 **Open Website** | "Open github.com" |
| 😄 **Jokes** | "Tell me a joke" |
| 🔊 **Volume** | "Set volume to 50" |

### Adding Custom Tools

Add your own tools in [`tools.py`](tools.py):

```python
def my_custom_tool(**kwargs) -> str:
    """Your tool logic here."""
    return "Result of your tool"

# Register it in the TOOLS dictionary:
TOOLS["my_tool"] = {
    "function": my_custom_tool,
    "description": "What it does",
    "keywords": ["trigger", "words"],
}
```

---

## 🌍 Multilingual Support

Mekuria supports **99+ languages** out of the box:

1. **Set STT language** in `config.py` → `STT_LANGUAGE = "am"` (Amharic example)
2. **Set TTS voice** → `TTS_VOICE = "am-ET-AmehaNeural"`
3. **Update persona** → Add language instructions to `SYSTEM_INSTRUCTION`

---

## 🆓 Free API & Tool Options

| Component | Free Option | Type |
|-----------|-----------|------|
| **LLM Brain** | [Google Gemini](https://aistudio.google.com/) | Cloud (free tier) |
| **LLM Brain** | [Groq](https://groq.com/) | Cloud (free tier, ultra-fast) |
| **LLM Brain** | [Ollama](https://ollama.com/) | 100% local & offline |
| **STT** | Faster-Whisper | Local & offline |
| **STT** | Groq Whisper API | Cloud (free tier) |
| **TTS** | Edge-TTS | Free neural voices |
| **TTS** | [Piper TTS](https://github.com/rhasspy/piper) | Local & offline |
| **Wake Word** | openWakeWord | Local & offline |

---

## 🛣️ Roadmap

- [ ] **Gemini Function Calling** — Let the LLM decide which tool to invoke
- [ ] **Smart Home Integration** — Control lights, thermostat, etc.
- [ ] **Visual HUD** — Holographic-style UI with PyQt or web frontend
- [ ] **Calendar & Email** — Read and manage your schedule
- [ ] **Music Control** — Play, pause, skip tracks
- [ ] **Ollama Support** — Fully offline LLM backend
- [ ] **Groq Backend** — Ultra-fast inference option
- [ ] **Custom Wake Word** — Train "Hey Mekuria"

---

## 📄 License

This project is open source. Built with ❤️ by you.
