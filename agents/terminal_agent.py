"""
╔══════════════════════════════════════════════════════════════╗
║           M E K U R I A   AI   A S S I S T A N T            ║
║            Terminal & Command Center Agent                   ║
╚══════════════════════════════════════════════════════════════╝
Executes shell commands (PowerShell, CMD, Bash, Git, Python, npm, Docker),
reads output, diagnoses errors, checks disk/network/ports, and enforces
security policies for dangerous commands.
"""

import subprocess
import os
import sys
from typing import Dict, Any, Tuple
from agents.base_agent import BaseAgent
from core.security import security
from core.emergency import check_emergency

class TerminalAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="TerminalAgent",
            description="Executes shell commands safely, reads output, and diagnoses failures."
        )

    def execute(self, command: str, cwd: str = None, timeout: int = 60) -> Tuple[int, str, str]:
        """Execute a shell command with security validation and error capture."""
        check_emergency()
        
        # 1. Check dangerous commands with security confirmation
        if security.is_dangerous_command(command):
            if not security.request_confirmation(f"Execute high-risk command: `{command}`", risk_level="HIGH"):
                return -1, "", "Command execution denied by security policy."

        self.log_step("Executing Command", command)

        try:
            res = subprocess.run(
                ["powershell", "-NoProfile", "-Command", command],
                cwd=cwd or os.getcwd(),
                capture_output=True,
                text=True,
                timeout=timeout
            )
            stdout = res.stdout.strip()
            stderr = res.stderr.strip()
            status = "SUCCESS" if res.returncode == 0 else "FAILED"
            security.audit_log(action="ExecuteCommand", tool="TerminalAgent", status=status, details=f"{command} (Exit: {res.returncode})")
            return res.returncode, stdout, stderr
        except subprocess.TimeoutExpired:
            return -2, "", f"Command timed out after {timeout} seconds."
        except Exception as e:
            return -3, "", f"Execution error: {e}"

    def run(self, goal: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        cmd = context.get("command", goal) if context else goal
        code, out, err = self.execute(cmd)
        return {
            "exit_code": code,
            "stdout": out,
            "stderr": err,
            "success": code == 0
        }

terminal_agent = TerminalAgent()
