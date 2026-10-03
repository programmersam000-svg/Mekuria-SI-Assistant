"""
╔══════════════════════════════════════════════════════════════╗
║           M E K U R I A   AI   A S S I S T A N T            ║
║              LLM Brain  — The Thinking Layer                 ║
╚══════════════════════════════════════════════════════════════╝
Uses Google Gemini API for reasoning, persona, and function calling.
Maintains conversation history for multi-turn dialogue.
"""

import sys

# Enforce UTF-8 output encoding on Windows consoles
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from google import genai
from google.genai import types
from rich.console import Console

import config

console = Console()

# ── Initialize the Gemini client ──────────────────────────────────
_client = None


def _get_client() -> genai.Client:
    global _client
    if _client is None:
        if not config.GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY not set! "
                "Add it to your .env file or set the environment variable."
            )
        _client = genai.Client(api_key=config.GEMINI_API_KEY)
        console.print("[cyan]Gemini client initialized.[/cyan]")
    return _client


# ── Conversation memory ───────────────────────────────────────────
_history: list[types.Content] = []


def _trim_history():
    """Keep only the last N turns to avoid exceeding context limits."""
    global _history
    max_messages = config.HISTORY_MAX_TURNS * 2  # user + assistant per turn
    if len(_history) > max_messages:
        _history = _history[-max_messages:]


def clear_history():
    """Reset the conversation history."""
    global _history
    _history = []
    console.print("[dim]Conversation history cleared.[/dim]")


def get_history() -> list:
    """Return a copy of the current conversation history."""
    return list(_history)


# ── Core thinking function ────────────────────────────────────────

def think(user_input: str) -> str:
    """
    Send user input to the Gemini LLM and return the assistant's reply.
    Maintains conversation history for contextual multi-turn dialogue.

    Args:
        user_input: The transcribed text from the user.

    Returns:
        The assistant's text response.
    """
    client = _get_client()

    # Build user content and append to history
    user_content = types.Content(
        role="user",
        parts=[types.Part.from_text(text=user_input)]
    )
    _history.append(user_content)
    _trim_history()

    try:
        response = client.models.generate_content(
            model=config.LLM_MODEL,
            contents=_history,
            config=types.GenerateContentConfig(
                system_instruction=config.SYSTEM_INSTRUCTION,
                temperature=config.LLM_TEMPERATURE,
            ),
        )

        reply = response.text.strip()

        # Build assistant content and append to history
        model_content = types.Content(
            role="model",
            parts=[types.Part.from_text(text=reply)]
        )
        _history.append(model_content)

        return reply

    except Exception as e:
        error_msg = f"I apologize, I encountered an error while processing: {e}"
        console.print(f"[red]LLM Error: {e}[/red]")
        return error_msg


# ── Quick one-shot query (no history) ─────────────────────────────

def ask_once(prompt: str) -> str:
    """
    Send a single prompt to the LLM without using conversation history.
    Useful for tool descriptions, summaries, or one-off queries.
    """
    client = _get_client()
    response = client.models.generate_content(
        model=config.LLM_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=config.SYSTEM_INSTRUCTION,
            temperature=config.LLM_TEMPERATURE,
        ),
    )
    return response.text.strip()


if __name__ == "__main__":
    # Quick test
    print(think("Hello Mekuria, who are you?"))
