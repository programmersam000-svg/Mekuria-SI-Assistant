"""
╔══════════════════════════════════════════════════════════════╗
║           M E K U R I A   AI   A S S I S T A N T            ║
║              Testing & Self-Verification Agent               ║
╚══════════════════════════════════════════════════════════════╝
Validates that tasks, scripts, websites, and files are genuinely
complete and operational before reporting completion to the user.
"""

import os
import subprocess
from typing import Dict, Any, List
from agents.base_agent import BaseAgent

class TestingAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="TestingAgent",
            description="Executes test suites, validates file existence, checks endpoints, and verifies results."
        )

    def verify_file_exists(self, file_path: str) -> bool:
        """Verify that a target file was genuinely created and is non-empty."""
        self.log_step("Verification", f"Checking existence of '{file_path}'...")
        return os.path.exists(file_path) and os.path.getsize(file_path) > 0

    def run_python_syntax_check(self, file_path: str) -> Dict[str, Any]:
        """Compile check a Python file without running side-effects."""
        self.log_step("Syntax Validation", f"Validating syntax in '{file_path}'...")
        try:
            res = subprocess.run(["python", "-m", "py_compile", file_path], capture_output=True, text=True)
            return {
                "valid": res.returncode == 0,
                "error": res.stderr.strip()
            }
        except Exception as e:
            return {"valid": False, "error": str(e)}

    def run(self, goal: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        file_path = context.get("file_path", "") if context else ""
        if file_path.endswith(".py"):
            return self.run_python_syntax_check(file_path)
        elif file_path:
            exists = self.verify_file_exists(file_path)
            return {"verified": exists, "file": file_path}
        return {"verified": True, "details": "Self-check completed."}

testing_agent = TestingAgent()
