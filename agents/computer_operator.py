"""
╔══════════════════════════════════════════════════════════════╗
║           M E K U R I A   AI   A S S I S T A N T            ║
║              Computer Operator & Screen Vision Agent         ║
╚══════════════════════════════════════════════════════════════╝
Acts as the hands and eyes of the computer: captures screenshots,
opens/closes applications, reads/writes clipboard, manages windows,
and triggers desktop controls.
"""

import os
import subprocess
import datetime
from typing import Dict, Any
from agents.base_agent import BaseAgent
from core.security import security

class ComputerOperatorAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="ComputerOperator",
            description="Controls desktop applications, captures screen, and manipulates clipboard/windows."
        )

    def capture_screen(self) -> str:
        """Capture full screen and save to Desktop."""
        self.log_step("Screen Vision", "Capturing desktop screenshot...")
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        filename = f"mekuria_screenshot_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        filepath = os.path.join(desktop, filename)

        ps_script = (
            "Add-Type -AssemblyName System.Windows.Forms, System.Drawing; "
            "$screen = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds; "
            "$bitmap = New-Object System.Drawing.Bitmap $screen.Width, $screen.Height; "
            "$graphics = [System.Drawing.Graphics]::FromImage($bitmap); "
            "$graphics.CopyFromScreen($screen.Location, [System.Drawing.Point]::Empty, $screen.Size); "
            f"$bitmap.Save('{filepath.replace('\\', '/')}'); "
            "$graphics.Dispose(); $bitmap.Dispose()"
        )

        try:
            subprocess.run(["powershell", "-NoProfile", "-Command", ps_script], capture_output=True, timeout=10)
            return filepath
        except Exception as e:
            return f"Screenshot failed: {e}"

    def launch_app(self, app_name: str) -> str:
        """Launch Windows application."""
        self.log_step("Application Control", f"Launching '{app_name}'...")
        import tools
        return tools.open_application(app_name)

    def close_app(self, process_name: str) -> str:
        """Close an application process."""
        self.log_step("Application Control", f"Closing '{process_name}'...")
        if not security.request_confirmation(f"Close process: {process_name}", risk_level="MEDIUM"):
            return "Action cancelled by user."
        try:
            subprocess.run(["powershell", "-NoProfile", "-Command", f"Stop-Process -Name '{process_name}' -Force -ErrorAction SilentlyContinue"], capture_output=True)
            return f"Process '{process_name}' terminated."
        except Exception as e:
            return f"Could not close process: {e}"

    def run(self, goal: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        lower = goal.lower()
        if "screenshot" in lower or "screen" in lower:
            path = self.capture_screen()
            return {"action": "screenshot", "result": path}
        elif "close" in lower or "kill" in lower:
            app = context.get("app", goal.replace("close", "").strip()) if context else goal.replace("close", "").strip()
            return {"action": "close", "result": self.close_app(app)}
        else:
            app = context.get("app", goal) if context else goal
            return {"action": "launch", "result": self.launch_app(app)}

computer_operator = ComputerOperatorAgent()
