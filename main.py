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
║            Ultimate Personal AI Operating Assistant                  ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝

Unified entry point:
  - 🤖 Autonomous Agent Mode (Multi-Step Goal Decomposition)
  - 💬 Interactive Conversational Assistant (5 Control Modes)
  - 🎤 Full Voice Assistant (Faster-Whisper + Edge-TTS)
  - 🛡️ Developer Mission Control & System HUD
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
from rich.table import Table

import config
import stt
import tts
import brain
import tools
import wake_word

from core.modes import ModeManager, OperatingMode
from core.emergency import emergency_stop
from core.orchestrator import orchestrator
from core.memory import memory
from ui.console_dashboard import run_developer_console

console = Console()

BANNER = """
[bold cyan]
   ███╗   ███╗███████╗██╗  ██╗██╗   ██╗██████╗ ██╗ █████╗ 
   ████╗ ████║██╔════╝██║ ██╔╝██║   ██║██╔══██╗██║██╔══██╗
   ██╔████╔██║█████╗  █████╔╝ ██║   ██║██████╔╝██║███████║
   ██║╚██╔╝██║██╔══╝  ██╔═██╗ ██║   ██║██╔══██╗██║██╔══██║
   ██║ ╚═╝ ██║███████╗██║  ██╗╚██████╔╝██║  ██║██║██║  ██║
   ╚═╝     ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝╚═╝  ╚═╝
[/bold cyan]
[dim]   Ultimate Personal AI Operating Assistant — Powered by Gemini[/dim]
"""

def print_banner():
    console.print(BANNER)
    console.print(
        Panel(
            f"[bold]Active Mode:[/bold] {ModeManager.get_mode().value}  |  "
            f"[bold]Voice:[/bold] {config.TTS_VOICE}  |  "
            f"[bold]Model:[/bold] {config.LLM_MODEL}  |  "
            f"[bold]Emergency Stop:[/bold] [green]ARMED[/green] ('STOP MEKURIA')",
            title="System Status",
            border_style="cyan",
        )
    )
    console.print()

def handle_personal_commands(user_input: str) -> str | None:
    """Handle special customized workflow macros (Req 45)."""
    lower = user_input.lower().strip()

    # 1. Emergency Stop
    if lower in ("stop mekuria", "emergency stop", "stop", "abort"):
        emergency_stop.trigger_stop("User invoked emergency stop")
        return "Emergency stop activated. All operations halted."

    # 2. Reset Emergency
    if lower in ("reset stop", "resume mekuria", "enable mekuria"):
        emergency_stop.reset()
        return "Emergency stop cleared. Mekuria is back online."

    # 3. Mode switching commands
    if lower in ("chat mode", "assist mode", "agent mode", "autonomous mode", "safe mode"):
        new_mode = lower.replace(" mode", "").upper()
        ModeManager.set_mode(new_mode)
        return f"Switched operating mode to {new_mode}."

    # 4. Good morning Mekuria
    if "good morning" in lower and "mekuria" in lower:
        telemetry = tools.get_system_telemetry()
        weather = tools.get_weather()
        return f"Good morning! System status: {telemetry}. {weather}. Ready for today's tasks."

    # 5. Work / Developer Mode
    if "work mode" in lower or "developer mode" in lower:
        tools.open_application("vscode")
        tools.open_application("terminal")
        ModeManager.set_mode(OperatingMode.AGENT)
        return "Work mode activated. Launched development environment and set AGENT mode."

    return None

def process_command(user_input: str) -> str:
    """Unified command and goal processor."""
    # Check personal commands & emergency stop
    special_reply = handle_personal_commands(user_input)
    if special_reply:
        return special_reply

    # Check for exit commands
    lower = user_input.lower().strip()
    if lower in ("exit", "quit", "goodbye", "bye", "shutdown mekuria"):
        return "__EXIT__"

    if lower in ("clear", "reset memory", "forget"):
        memory.clear_short_term()
        brain.clear_history()
        return "Memory cleared. Starting a fresh session."

    # In Autonomous or Agent Mode, if goal is multi-step (e.g. "Build", "Create", "Research")
    if ModeManager.is_autonomous() and any(trigger in lower for trigger in ["build", "create", "research", "develop", "scaffold", "diagnose"]):
        console.print("[dim]⚡ Activating Autonomous Multi-Agent Orchestrator...[/dim]")
        res = orchestrator.execute_goal(user_input)
        status = "Completed and verified" if res.get("verified") else "Completed with warnings"
        return f"Task '{user_input[:40]}' has been processed autonomously. Status: {status}."

    # Attempt tool matching
    tool_name, tool_func = tools.match_tool(user_input)
    if tool_name:
        console.print(f"[dim]Executing tool: {tool_name}[/dim]")
        tool_result = tools.execute_tool(tool_name, user_input)
        narration_prompt = (
            f"The user said: \"{user_input}\"\n"
            f"Tool '{tool_name}' result:\n{tool_result}\n\n"
            f"Respond naturally, concisely, and conversationally."
        )
        return brain.think(narration_prompt)

    # Standard conversational thinking
    return brain.think(user_input)

def voice_loop():
    """Continuous voice assistant execution loop."""
    print_banner()
    console.print("[bold green]🎤 Voice mode activated. Speak into your microphone![/bold green]")
    console.print("[dim]Say 'goodbye' or 'exit' to quit.[/dim]\n")

    greeting = f"Hello! I am {config.ASSISTANT_NAME}, your personal AI operating assistant. How may I help you today?"
    console.print(f"[bold cyan]{config.ASSISTANT_NAME}:[/bold cyan] {greeting}")
    tts.speak(greeting)

    while True:
        try:
            if not wake_word.wait_for_wake_word():
                break

            user_text = stt.listen()
            if not user_text:
                continue

            reply = process_command(user_text)

            if reply == "__EXIT__":
                farewell = "Goodbye! Shutting down."
                console.print(f"[bold cyan]{config.ASSISTANT_NAME}:[/bold cyan] {farewell}")
                tts.speak(farewell)
                break

            console.print(f"\n[bold cyan]{config.ASSISTANT_NAME}:[/bold cyan] {reply}")
            tts.speak(reply)

        except KeyboardInterrupt:
            console.print("\n[yellow]Voice mode closed.[/yellow]")
            break

def text_loop():
    """Interactive command center and chat loop."""
    print_banner()
    console.print("[bold green]⌨️  Interactive Command Center activated.[/bold green]")
    console.print("[dim]Commands: 'agent mode', 'safe mode', 'work mode', 'hud', 'exit'[/dim]\n")

    greeting = f"Mekuria online. Active mode: {ModeManager.get_mode().value}. How may I assist you?"
    console.print(f"[bold cyan]{config.ASSISTANT_NAME}:[/bold cyan] {greeting}")
    tts.speak(greeting)

    while True:
        try:
            user_input = console.input(f"\n[bold yellow]You ({ModeManager.get_mode().value}):[/bold yellow] ").strip()
            if not user_input:
                continue

            if user_input.lower() == "hud" or user_input.lower() == "console":
                run_developer_console()
                continue

            if user_input.lower() == "voice":
                voice_loop()
                return

            reply = process_command(user_input)

            if reply == "__EXIT__":
                farewell = "Goodbye! Session terminated."
                console.print(f"[bold cyan]{config.ASSISTANT_NAME}:[/bold cyan] {farewell}")
                tts.speak(farewell)
                break

            console.print(f"\n[bold cyan]{config.ASSISTANT_NAME}:[/bold cyan] {reply}")
            tts.speak(reply)

        except KeyboardInterrupt:
            console.print("\n[yellow]Session closed.[/yellow]")
            break
        except EOFError:
            break

def main():
    args = sys.argv[1:]

    if "--help" in args or "-h" in args:
        console.print(Panel(
            "[bold]Mekuria CLI Options:[/bold]\n\n"
            "  python main.py             -> Interactive Command Center (Default)\n"
            "  python main.py --voice     -> Full Voice Assistant\n"
            "  python main.py --console   -> Developer Mission Control Dashboard\n"
            "  python main.py --agent     -> Autonomous Agent Mode for target goal\n",
            title="Mekuria AI Assistant",
            border_style="cyan",
        ))
        return

    if "--voice" in args or "-v" in args:
        voice_loop()
    elif "--console" in args or "--hud" in args:
        run_developer_console()
    elif "--agent" in args:
        ModeManager.set_mode(OperatingMode.AUTONOMOUS)
        goal = " ".join(args[args.index("--agent") + 1:]) if len(args) > args.index("--agent") + 1 else "Perform system audit and health check"
        orchestrator.execute_goal(goal)
    else:
        text_loop()

if __name__ == "__main__":
    main()
