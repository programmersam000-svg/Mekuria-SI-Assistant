"""
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║           ███╗   ███╗███████╗██╗  ██╗██╗   ██╗██████╗ ██╗ █████╗     ║
║           ████╗ ████║██╔════╝██║ ██╔╝██║   ██║██╔══██╗██║██╔══██╗   ║
║           ██╔████╔██║█████╗  █████╔╝ ██║   ██║██████╔╝██║███████║   ║
║           ██║╚██╔╝██║██╔══╝  ██╔═██╗ ██║   ██║██╔══██╗██║██╔══██║   ║
║           ██║ ╚═╝ ██║███████╗██║  ██╗╚██████╔╝██║  ██║██║██║  ██║   ║
║           ╚═╝     ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝╚═╝  ╚═╝   ║
║                                                                      ║
║                Your Personal AI Assistant                            ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝

Main entry point — connects all four layers:
  Speech-to-Text  (stt.py)     ->  Hearing Layer
  LLM Reasoning   (brain.py)   ->  Thinking Layer
  Tool Execution  (tools.py)   ->  Execution Layer
  Text-to-Speech  (tts.py)     ->  Speaking Layer
"""

import sys
import os

# Enforce UTF-8 output encoding on Windows consoles
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from rich.console import Console
from rich.panel import Panel

import config
import stt
import tts
import brain
import tools
import wake_word

console = Console()


# ══════════════════════════════════════════════════════════════════
#  BANNER
# ══════════════════════════════════════════════════════════════════

BANNER = """
[bold cyan]
   ███╗   ███╗███████╗██╗  ██╗██╗   ██╗██████╗ ██╗ █████╗ 
   ████╗ ████║██╔════╝██║ ██╔╝██║   ██║██╔══██╗██║██╔══██╗
   ██╔████╔██║█████╗  █████╔╝ ██║   ██║██████╔╝██║███████║
   ██║╚██╔╝██║██╔══╝  ██╔═██╗ ██║   ██║██╔══██╗██║██╔══██║
   ██║ ╚═╝ ██║███████╗██║  ██╗╚██████╔╝██║  ██║██║██║  ██║
   ╚═╝     ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝╚═╝  ╚═╝
[/bold cyan]
[dim]   Your Personal AI Assistant — Powered by Gemini[/dim]
"""


def print_banner():
    console.print(BANNER)
    console.print(
        Panel(
            f"[bold]Voice:[/bold] {config.TTS_VOICE}  |  "
            f"[bold]Model:[/bold] {config.LLM_MODEL}  |  "
            f"[bold]Whisper:[/bold] {config.WHISPER_MODEL_SIZE}  |  "
            f"[bold]Wake Word:[/bold] {'ON' if config.WAKE_WORD_ENABLED else 'OFF'}",
            title="Configuration",
            border_style="cyan",
        )
    )
    console.print()


# ══════════════════════════════════════════════════════════════════
#  PROCESSING PIPELINE
# ══════════════════════════════════════════════════════════════════

def process_command(user_input: str) -> str:
    """
    Process a user command through the full pipeline:
    1. Check if a built-in tool matches
    2. If yes -> execute tool, then let the LLM narrate the result
    3. If no  -> send directly to the LLM for a conversational reply
    """
    # Check for exit commands
    lower = user_input.lower().strip()
    if lower in ("exit", "quit", "goodbye", "bye", "stop", "shut down mekuria"):
        return "__EXIT__"

    if lower in ("clear", "reset", "forget", "new conversation"):
        brain.clear_history()
        return "Memory cleared. Starting a fresh conversation."

    # Attempt tool matching
    tool_name, tool_info = tools.match_tool(user_input)

    if tool_name:
        console.print(f"[dim]Executing tool: {tool_name}[/dim]")
        tool_result = tools.execute_tool(tool_name, user_input)

        # Let the LLM narrate the tool result naturally
        narration_prompt = (
            f"The user said: \"{user_input}\"\n"
            f"You executed the '{tool_name}' tool and got this result:\n"
            f"{tool_result}\n\n"
            f"Now respond naturally to the user, incorporating the tool result "
            f"in your characteristic style. Be brief."
        )
        return brain.think(narration_prompt)

    # No tool matched — pure conversation
    return brain.think(user_input)


# ══════════════════════════════════════════════════════════════════
#  VOICE MODE — Full voice loop
# ══════════════════════════════════════════════════════════════════

def voice_loop():
    """
    Main voice assistant loop:
      [Wake Word] -> Listen -> Think -> Act -> Speak -> Repeat
    """
    print_banner()
    console.print("[bold green]Voice mode activated. Speak to interact![/bold green]")
    console.print("[dim]Say 'goodbye' or 'exit' to quit.[/dim]\n")

    # Greeting
    greeting = f"Hello! I am {config.ASSISTANT_NAME}, your personal AI assistant. How may I help you today?"
    console.print(f"[bold cyan]{config.ASSISTANT_NAME}:[/bold cyan] {greeting}")
    tts.speak(greeting)

    while True:
        try:
            # 1. Wait for wake word (if enabled)
            if not wake_word.wait_for_wake_word():
                break

            # 2. Listen (STT)
            user_text = stt.listen()
            if not user_text:
                console.print("[dim]Didn't catch that. Try again.[/dim]")
                continue

            # 3. Think + Act
            reply = process_command(user_text)

            if reply == "__EXIT__":
                farewell = "Goodbye! It was a pleasure assisting you. Until next time."
                console.print(f"[bold cyan]{config.ASSISTANT_NAME}:[/bold cyan] {farewell}")
                tts.speak(farewell)
                break

            # 4. Speak
            console.print(f"\n[bold cyan]{config.ASSISTANT_NAME}:[/bold cyan] {reply}")
            tts.speak(reply)

        except KeyboardInterrupt:
            console.print("\n[yellow]Interrupted. Shutting down...[/yellow]")
            tts.speak("Shutting down. Goodbye!")
            break


# ══════════════════════════════════════════════════════════════════
#  TEXT MODE — Type-based interaction (no microphone needed)
# ══════════════════════════════════════════════════════════════════

def text_loop():
    """
    Text-only interaction mode.
    Type your queries and Mekuria responds with text + speech.
    Useful when you don't have a microphone or prefer typing.
    """
    print_banner()
    console.print("[bold green]Text mode activated. Type to interact![/bold green]")
    console.print("[dim]Type 'exit' to quit  |  'voice' to switch to voice mode[/dim]\n")

    greeting = f"Hello! I am {config.ASSISTANT_NAME}. How may I assist you today?"
    console.print(f"[bold cyan]{config.ASSISTANT_NAME}:[/bold cyan] {greeting}")
    tts.speak(greeting)

    while True:
        try:
            user_input = console.input(f"\n[bold yellow]You:[/bold yellow] ").strip()

            if not user_input:
                continue

            if user_input.lower() == "voice":
                voice_loop()
                return

            reply = process_command(user_input)

            if reply == "__EXIT__":
                farewell = "Goodbye! It was a pleasure assisting you."
                console.print(f"[bold cyan]{config.ASSISTANT_NAME}:[/bold cyan] {farewell}")
                tts.speak(farewell)
                break

            console.print(f"\n[bold cyan]{config.ASSISTANT_NAME}:[/bold cyan] {reply}")
            tts.speak(reply)

        except KeyboardInterrupt:
            console.print("\n[yellow]Goodbye![/yellow]")
            break
        except EOFError:
            break


# ══════════════════════════════════════════════════════════════════
#  ENTRY POINT
# ══════════════════════════════════════════════════════════════════

def main():
    """Parse command-line arguments and start the appropriate mode."""
    args = sys.argv[1:]

    if "--help" in args or "-h" in args:
        console.print(Panel(
            "[bold]Usage:[/bold]\n"
            f"  python main.py          -> Text mode (type to chat)\n"
            f"  python main.py --voice  -> Voice mode (speak to chat)\n"
            f"  python main.py --help   -> Show this help\n",
            title=f"{config.ASSISTANT_NAME} AI Assistant",
            border_style="cyan",
        ))
        return

    if "--voice" in args or "-v" in args:
        voice_loop()
    else:
        text_loop()


if __name__ == "__main__":
    main()
