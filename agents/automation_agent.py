"""
╔══════════════════════════════════════════════════════════════╗
║           M E K U R I A   AI   A S S I S T A N T            ║
║          Automation, Reminders & Communication Agent         ║
╚══════════════════════════════════════════════════════════════╝
Handles scheduled background automations, voice alarms, email drafting,
calendar event summaries, and system notifications.
"""

import threading
import time
from typing import Dict, Any, List
from agents.base_agent import BaseAgent
from core.emergency import check_emergency

class AutomationAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="AutomationAgent",
            description="Manages background timers, notifications, recurring automations, and calendar/email assistance."
        )

    def schedule_reminder(self, seconds: int, message: str):
        """Schedule a background reminder."""
        self.log_step("Scheduling Reminder", f"Timer set for {seconds}s: '{message}'")
        def _job():
            time.sleep(seconds)
            if check_emergency:
                try:
                    check_emergency()
                except InterruptedError:
                    return
            import tts
            tts.speak(f"Notification: {message}")

        t = threading.Thread(target=_job, daemon=True)
        t.start()
        return f"Reminder scheduled in {seconds} seconds."

    def draft_email(self, recipient: str, subject: str, core_message: str) -> str:
        """Draft a formal professional email."""
        self.log_step("Email Drafting", f"Drafting email to '{recipient}'...")
        draft = (
            f"To: {recipient}\n"
            f"Subject: {subject}\n\n"
            f"Dear Recipient,\n\n"
            f"{core_message}\n\n"
            f"Best regards,\n"
            f"Prepared on behalf of User via Mekuria Assistant"
        )
        return draft

    def run(self, goal: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        lower = goal.lower()
        if "timer" in lower or "remind" in lower:
            secs = context.get("seconds", 60) if context else 60
            msg = context.get("message", goal) if context else goal
            return {"status": self.schedule_reminder(secs, msg)}
        elif "email" in lower:
            to = context.get("recipient", "contact@example.com") if context else "contact@example.com"
            subj = context.get("subject", "Update") if context else "Update"
            return {"draft": self.draft_email(to, subj, goal)}
        return {"status": "Automation ready."}

automation_agent = AutomationAgent()
