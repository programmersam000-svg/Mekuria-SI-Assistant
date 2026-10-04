"""
╔══════════════════════════════════════════════════════════════╗
║           M E K U R I A   AI   A S S I S T A N T            ║
║              Operating Modes & Control Levels                ║
╚══════════════════════════════════════════════════════════════╝
Implements the 5 User Control Modes:
  1. CHAT MODE       — Answer queries without executing tools.
  2. ASSIST MODE     — Propose actions and wait for user approval.
  3. AGENT MODE      — Execute standard safe tasks autonomously.
  4. AUTONOMOUS MODE — Complete long-running complex multi-step goals.
  5. SAFE MODE       — Require confirmation before every significant operation.
"""

from enum import Enum
from rich.console import Console

console = Console()

class OperatingMode(str, Enum):
    CHAT = "CHAT"
    ASSIST = "ASSIST"
    AGENT = "AGENT"
    AUTONOMOUS = "AUTONOMOUS"
    SAFE = "SAFE"

class ModeManager:
    """Manages Mekuria's active operational mode."""
    _current_mode: OperatingMode = OperatingMode.AGENT

    @classmethod
    def get_mode(cls) -> OperatingMode:
        return cls._current_mode

    @classmethod
    def set_mode(cls, mode: OperatingMode | str):
        if isinstance(mode, str):
            mode = OperatingMode(mode.upper())
        cls._current_mode = mode
        console.print(f"[bold cyan]🎯 Operating Mode set to:[/bold cyan] [bold green]{cls._current_mode.value}[/bold green]")

    @classmethod
    def is_autonomous(cls) -> bool:
        return cls._current_mode in (OperatingMode.AGENT, OperatingMode.AUTONOMOUS)

    @classmethod
    def requires_approval_for_safe_actions(cls) -> bool:
        return cls._current_mode in (OperatingMode.ASSIST, OperatingMode.SAFE)

    @classmethod
    def is_chat_only(cls) -> bool:
        return cls._current_mode == OperatingMode.CHAT
