"""
╔══════════════════════════════════════════════════════════════╗
║           M E K U R I A   AI   A S S I S T A N T            ║
║              Global Emergency Stop Controller                ║
╚══════════════════════════════════════════════════════════════╝
Provides an immediate global kill-switch ("STOP MEKURIA") that halts
all background tasks, processes, browser automations, and subagents.
"""

import threading
import sys
from rich.console import Console

console = Console()

class EmergencyStopController:
    """Thread-safe global emergency stop controller."""
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._stop_event = threading.Event()
                cls._instance._listeners = []
            return cls._instance

    def trigger_stop(self, reason: str = "User Emergency Stop triggered"):
        """Trigger global emergency stop."""
        self._stop_event.set()
        console.print(f"\n[bold white on red] 🛑 EMERGENCY STOP ACTIVATED: {reason} [/bold white on red]")
        # Notify all registered process/thread hooks
        for listener in list(self._listeners):
            try:
                listener()
            except Exception as e:
                console.print(f"[red]Error notifying stop listener: {e}[/red]")

    def reset(self):
        """Reset emergency stop state."""
        self._stop_event.clear()
        console.print("[green]✅ Emergency stop reset. System ready.[/green]")

    def is_stopped(self) -> bool:
        """Check if emergency stop is currently active."""
        return self._stop_event.is_set()

    def register_listener(self, callback):
        """Register a callback hook to be executed immediately upon emergency stop."""
        if callback not in self._listeners:
            self._listeners.append(callback)

    def unregister_listener(self, callback):
        if callback in self._listeners:
            self._listeners.remove(callback)

# Singleton global instance
emergency_stop = EmergencyStopController()

def check_emergency():
    """Raise InterruptedError if emergency stop is engaged."""
    if emergency_stop.is_stopped():
        raise InterruptedError("Operation aborted by Mekuria Emergency Stop.")
