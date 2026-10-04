"""
╔══════════════════════════════════════════════════════════════╗
║           M E K U R I A   AI   A S S I S T A N T            ║
║              Extensible Skill / Plugin Manager               ║
╚══════════════════════════════════════════════════════════════╝
Discovers, dynamically loads, and manages installable skills & plugins
without requiring a full assistant rebuild or restart.
"""

import os
import importlib
from typing import Dict, Any, Callable
from rich.console import Console

console = Console()

class SkillManager:
    """Dynamic plugin and skill management engine."""

    def __init__(self):
        self._skills: Dict[str, Dict[str, Any]] = {}
        self._load_builtin_skills()

    def register_skill(self, name: str, description: str, handler: Callable, version: str = "1.0.0"):
        """Register a new active skill."""
        self._skills[name] = {
            "name": name,
            "description": description,
            "handler": handler,
            "version": version
        }
        console.print(f"[cyan]🧩 Skill Loaded:[/cyan] [bold]{name}[/bold] (v{version})")

    def _load_builtin_skills(self):
        """Register core baseline skills."""
        import tools
        self.register_skill("weather", "Fetch live city weather forecasts", tools.get_weather)
        self.register_skill("wikipedia", "Summarize Wikipedia encyclopedia topics", tools.search_wikipedia)
        self.register_skill("screenshot", "Capture desktop screen to file", tools.take_screenshot)
        self.register_skill("news", "Fetch top world & tech news headlines", tools.get_news_headlines)
        self.register_skill("calculator", "Evaluate safe mathematical formulas", tools.calculate_math)
        self.register_skill("telemetry", "Collect real-time CPU/RAM/Disk metrics", tools.get_system_telemetry)
        
        # Amharic Language & Tutoring Skills
        try:
            import amharic
            self.register_skill("amharic_lesson", "Generate structured 15-minute Amharic lesson", amharic.amharic_teacher.generate_daily_lesson)
            self.register_skill("fidel", "Explain Ethiopian Fidel families and orders", amharic.get_fidel_lesson)
            self.register_skill("amharic_coding", "Explain programming concepts in Amharic", amharic.explain_coding_concept)
        except Exception:
            pass

    def get_skills_list(self) -> Dict[str, str]:
        """Return dictionary of installed skill names and descriptions."""
        return {k: v["description"] for k, v in self._skills.items()}

    def execute_skill(self, name: str, *args, **kwargs) -> Any:
        """Execute a registered skill by name."""
        skill = self._skills.get(name)
        if not skill:
            raise KeyError(f"Skill '{name}' is not installed.")
        return skill["handler"](*args, **kwargs)

skill_manager = SkillManager()
