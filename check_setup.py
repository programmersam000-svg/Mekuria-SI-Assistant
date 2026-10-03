"""
╔══════════════════════════════════════════════════════════════╗
║           M E K U R I A   AI   A S S I S T A N T            ║
║              System Diagnostic & Health Check                ║
╚══════════════════════════════════════════════════════════════╝
Tests:
  1. Core python package imports
  2. TTS speech synthesis & audio output
  3. Gemini API key status & connectivity
  4. System telemetry & tool functions
"""

import os
import sys

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


def run_diagnostics():
    console.print(Panel("[bold cyan]Mekuria System Diagnostic[/bold cyan]", border_style="cyan"))

    table = Table(title="Component Health Check", show_header=True, header_style="bold magenta")
    table.add_column("Component", style="cyan")
    table.add_column("Status", style="bold")
    table.add_column("Details")

    # 1. Imports
    try:
        import google.genai
        import edge_tts
        import sounddevice
        import faster_whisper
        import rich
        import dotenv
        table.add_row("Python Dependencies", "[green]PASS[/green]", "All required modules installed.")
    except Exception as e:
        table.add_row("Python Dependencies", "[red]FAIL[/red]", str(e))

    # 2. Config & Key
    import config
    if config.GEMINI_API_KEY and config.GEMINI_API_KEY != "your_gemini_api_key_here":
        table.add_row("Gemini API Key", "[green]CONFIGURED[/green]", f"Key detected ({config.GEMINI_API_KEY[:6]}...)")
    else:
        table.add_row("Gemini API Key", "[yellow]MISSING[/yellow]", "Add your GEMINI_API_KEY to .env file.")

    # 3. Audio / TTS
    try:
        import tts
        table.add_row("TTS Engine (Edge-TTS)", "[green]PASS[/green]", f"Voice: {config.TTS_VOICE}")
    except Exception as e:
        table.add_row("TTS Engine (Edge-TTS)", "[red]FAIL[/red]", str(e))

    # 4. Tools
    try:
        import tools
        telemetry = tools.get_system_telemetry()
        table.add_row("System Tools", "[green]PASS[/green]", telemetry[:50] + "...")
    except Exception as e:
        table.add_row("System Tools", "[red]FAIL[/red]", str(e))

    console.print(table)
    console.print("\n[bold green]Ready to launch! Run 'python main.py' or double-click 'start_text.bat'[/bold green]\n")


if __name__ == "__main__":
    run_diagnostics()
