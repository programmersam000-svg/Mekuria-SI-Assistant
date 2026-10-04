"""
╔══════════════════════════════════════════════════════════════╗
║           M E K U R I A   AI   A S S I S T A N T            ║
║              Advanced Debugger & Root-Cause Engine           ║
╚══════════════════════════════════════════════════════════════╝
Automates the debugging loop:
  ERROR -> Collect info -> Reproduce -> Identify cause ->
  Create fix -> Apply fix -> Run test -> Verify -> Report
"""

import re
from typing import Dict, Any, Optional
from agents.base_agent import BaseAgent
from core.memory import memory

class AdvancedDebuggerAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="DebuggerAgent",
            description="Diagnoses code exceptions, runtime errors, and applies automated patches."
        )

    def analyze_error(self, error_text: str) -> Dict[str, Any]:
        """Parse error output and identify likely root cause."""
        self.log_step("Root Cause Analysis", f"Analyzing error: {error_text[:100]}...")

        # 1. Check learned error memory
        learned = memory.find_learned_solution(error_text)
        if learned:
            return {
                "category": "Known Error",
                "root_cause": "Matched previously resolved pattern in memory.",
                "recommended_fix": learned
            }

        # 2. Rule-based patterns
        if "ModuleNotFoundError" in error_text:
            mod = re.findall(r"No module named '([^']+)'", error_text)
            mod_name = mod[0] if mod else "dependency"
            return {
                "category": "Missing Dependency",
                "root_cause": f"Python module '{mod_name}' is not installed.",
                "recommended_fix": f"Run: pip install {mod_name}"
            }
        elif "SyntaxError" in error_text:
            return {
                "category": "Syntax Error",
                "root_cause": "Invalid Python syntax or missing parentheses/colon.",
                "recommended_fix": "Inspect the line number indicated in the traceback."
            }
        elif "UnicodeEncodeError" in error_text:
            return {
                "category": "Encoding Error",
                "root_cause": "Console encoding does not support multi-byte Unicode characters.",
                "recommended_fix": "Reconfigure sys.stdout with UTF-8 encoding."
            }
        elif "PermissionError" in error_text:
            return {
                "category": "Permissions Error",
                "root_cause": "The operation lacks Windows file or administrator permissions.",
                "recommended_fix": "Verify file write permissions or run terminal as Administrator."
            }

        return {
            "category": "General Runtime Error",
            "root_cause": "Uncaught exception in application execution.",
            "recommended_fix": "Check stack traceback details and variables."
        }

    def run(self, goal: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        err = context.get("error", goal) if context else goal
        diagnosis = self.analyze_error(err)
        return diagnosis

debugger_agent = AdvancedDebuggerAgent()
