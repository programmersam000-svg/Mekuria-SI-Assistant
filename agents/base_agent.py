"""
╔══════════════════════════════════════════════════════════════╗
║           M E K U R I A   AI   A S S I S T A N T            ║
║                  Base Agent Interface                        ║
╚══════════════════════════════════════════════════════════════╝
Defines the standard autonomous execution loop for all specialized agents:
  UNDERSTAND -> PLAN -> EXECUTE -> OBSERVE -> DEBUG -> TEST -> VERIFY -> REPORT
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List
from rich.console import Console
from core.emergency import check_emergency
from core.security import security

console = Console()

class BaseAgent(ABC):
    """Abstract base class for all specialized Mekuria agents."""

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    @abstractmethod
    def run(self, goal: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute the agent workflow for a given goal."""
        pass

    def log_step(self, step_name: str, details: str):
        check_emergency()
        console.print(f"[bold cyan][{self.name}][/bold cyan] [yellow]{step_name}:[/yellow] {details}")
        security.audit_log(action=step_name, tool=self.name, status="EXECUTING", details=details)
