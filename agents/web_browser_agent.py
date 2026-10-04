"""
╔══════════════════════════════════════════════════════════════╗
║           M E K U R I A   AI   A S S I S T A N T            ║
║           Web Browser & Form Filling Automation Agent        ║
╚══════════════════════════════════════════════════════════════╝
Automates web browsing, searches target websites, extracts webpage text,
and prepares structured form submission payloads with confirmation safeguards.
"""

import urllib.request
import urllib.parse
import re
import webbrowser
from typing import Dict, Any, List
from agents.base_agent import BaseAgent
from core.security import security

class WebBrowserAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="WebBrowserAgent",
            description="Navigates websites, extracts page text, and assists with form data preparation."
        )

    def fetch_webpage_text(self, url: str) -> str:
        """Fetch static text content from a web URL."""
        self.log_step("Web Navigation", f"Fetching content from '{url}'...")
        if not url.startswith(("http://", "https://")):
            url = "https://" + url

        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
            with urllib.request.urlopen(req, timeout=10) as response:
                html = response.read().decode("utf-8", errors="replace")
                # Strip scripts and styles
                clean = re.sub(r"<(script|style).*?>.*?</\1>", "", html, flags=re.DOTALL | re.IGNORECASE)
                # Strip tags
                text = re.sub(r"<[^>]+>", " ", clean)
                # Normalize whitespace
                text = re.sub(r"\s+", " ", text).strip()
                return text[:5000]
        except Exception as e:
            return f"Failed to fetch webpage: {e}"

    def prepare_form_submission(self, form_name: str, form_fields: Dict[str, str]) -> Dict[str, Any]:
        """Review and prepare form data with user confirmation safeguard."""
        self.log_step("Form Filling", f"Validating form '{form_name}' with {len(form_fields)} fields...")
        
        # Check for missing/empty fields
        missing = [k for k, v in form_fields.items() if not v]
        
        # Require confirmation before submitting important applications
        authorized = security.request_confirmation(
            f"Submit form '{form_name}' with payload: {form_fields}",
            risk_level="HIGH"
        )

        return {
            "form_name": form_name,
            "missing_fields": missing,
            "submission_authorized": authorized,
            "status": "Ready to submit" if authorized and not missing else "Pending completion/authorization"
        }

    def run(self, goal: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        url = context.get("url", "") if context else ""
        if url:
            return {"url": url, "content": self.fetch_webpage_text(url)}
        import tools
        return {"action": "open_browser", "result": tools.open_website(goal)}

web_browser_agent = WebBrowserAgent()
