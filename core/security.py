"""
╔══════════════════════════════════════════════════════════════╗
║           M E K U R I A   AI   A S S I S T A N T            ║
║              Security Center & Smart Confirmation            ║
╚══════════════════════════════════════════════════════════════╝
Enforces least-privilege execution, smart confirmation policies for
dangerous actions (file deletions, system modifications, secret protection),
and full immutable audit logging.
"""

import os
import datetime
import re
from typing import Optional, Callable
from rich.console import Console
from rich.panel import Panel
from core.modes import ModeManager, OperatingMode
from core.emergency import emergency_stop

console = Console()

AUDIT_LOG_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "audit_log.txt")

# Operations classified as high-risk requiring explicit user confirmation
DANGEROUS_COMMAND_PATTERNS = [
    r"\brm\s+-rf\b",
    r"\bdel\s+/[sfq]\b",
    r"\bformat\b",
    r"\bdiskpart\b",
    r"\bshutdown\b",
    r"\brestart-computer\b",
    r"\bRemove-Item\s+.*-Recurse\b",
    r"\bdrop\s+database\b",
    r"\bdrop\s+table\b",
    r"\btruncate\b",
    r"\bgit\s+reset\s+--hard\b",
    r"\bgit\s+clean\s+-fdx\b",
]

SENSITIVE_SECRET_PATTERNS = [
    r"ghp_[A-Za-z0-9_]{30,}",
    r"sk-[A-Za-z0-9_]{30,}",
    r"AIza[0-9A-Za-z-_]{35}",
    r"password\s*=\s*['\"][^'\"]+['\"]",
]

class SecurityCenter:
    """Central security and policy engine for Mekuria."""

    @staticmethod
    def mask_secrets(text: str) -> str:
        """Sanitize text to prevent accidental exposure of tokens or passwords."""
        masked = text
        for pattern in SENSITIVE_SECRET_PATTERNS:
            masked = re.sub(pattern, "[PROTECTED_SECRET]", masked)
        return masked

    @staticmethod
    def is_dangerous_command(command: str) -> bool:
        """Check if command matches high-risk destructive patterns."""
        for pattern in DANGEROUS_COMMAND_PATTERNS:
            if re.search(pattern, command, re.IGNORECASE):
                return True
        return False

    @staticmethod
    def audit_log(action: str, tool: str, status: str, details: str = ""):
        """Append an entry to the immutable audit log."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sanitized_details = SecurityCenter.mask_secrets(details)
        log_entry = f"[{timestamp}] | ACTION: {action} | TOOL: {tool} | STATUS: {status} | DETAILS: {sanitized_details}\n"

        os.makedirs(os.path.dirname(AUDIT_LOG_FILE), exist_ok=True)
        try:
            with open(AUDIT_LOG_FILE, "a", encoding="utf-8") as f:
                f.write(log_entry)
        except Exception:
            pass

    @classmethod
    def request_confirmation(cls, action_description: str, risk_level: str = "HIGH") -> bool:
        """
        Smart confirmation check.
        In SAFE mode or for high-risk actions, prompts the user interactively.
        """
        if emergency_stop.is_stopped():
            return False

        current_mode = ModeManager.get_mode()

        # In CHAT mode, no actions permitted
        if current_mode == OperatingMode.CHAT:
            console.print("[yellow]Action blocked: Mekuria is in CHAT mode.[/yellow]")
            return False

        # In SAFE mode, always ask
        # In other modes, only ask if risk_level is HIGH or action is dangerous
        requires_prompt = (
            current_mode == OperatingMode.SAFE or
            current_mode == OperatingMode.ASSIST or
            risk_level.upper() in ("HIGH", "CRITICAL")
        )

        if not requires_prompt:
            return True

        console.print(Panel(
            f"[bold yellow]⚠️  CONFIRMATION REQUIRED ({risk_level} RISK)[/bold yellow]\n\n"
            f"[bold white]{action_description}[/bold white]\n\n"
            f"Do you authorize Mekuria to proceed? (y/N): ",
            title="🔐 Security Permission",
            border_style="yellow"
        ))

        try:
            choice = input().strip().lower()
            authorized = choice in ("y", "yes")
            cls.audit_log(
                action=action_description,
                tool="SecurityGate",
                status="AUTHORIZED" if authorized else "DENIED",
                details=f"User prompt response: {choice}"
            )
            return authorized
        except (EOFError, KeyboardInterrupt):
            return False

security = SecurityCenter()
