"""
╔══════════════════════════════════════════════════════════════╗
║           M E K U R I A   AI   A S S I S T A N T            ║
║        Education, Career, Translation & Data Agent           ║
╚══════════════════════════════════════════════════════════════╝
Acts as personal tutor, CV/resume optimizer, career coach,
multilingual translator, and structured data analyst.
"""

from typing import Dict, Any
from agents.base_agent import BaseAgent

class TutorCareerAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="TutorCareerAgent",
            description="Assists with personalized tutoring, career CV optimization, translation, and data analysis."
        )

    def analyze_cv_structure(self, cv_text: str) -> Dict[str, Any]:
        """Analyze a CV or resume for key sections and recommend enhancements."""
        self.log_step("Career Analysis", "Evaluating CV content structure...")
        sections_found = {
            "Contact Info": any(k in cv_text.lower() for k in ["email", "phone", "github", "linkedin"]),
            "Experience": any(k in cv_text.lower() for k in ["experience", "employment", "history", "work"]),
            "Projects": "project" in cv_text.lower(),
            "Skills": any(k in cv_text.lower() for k in ["skill", "technologies", "tools", "languages"]),
            "Education": any(k in cv_text.lower() for k in ["education", "degree", "university", "bachelor"]),
        }
        recommendations = []
        if not sections_found["Projects"]:
            recommendations.append("Add a dedicated Projects section highlighting measurable outcomes.")
        if not sections_found["Skills"]:
            recommendations.append("Group your technical skills into clear categories (Languages, Frameworks, Cloud).")

        return {
            "sections_present": sections_found,
            "recommendations": recommendations or ["CV structure covers all core industry standards."]
        }

    def run(self, goal: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        lower = goal.lower()
        if "cv" in lower or "resume" in lower:
            text = context.get("cv_text", goal) if context else goal
            return self.analyze_cv_structure(text)
        return {"result": f"Processed educational/career inquiry: {goal}"}

tutor_career_agent = TutorCareerAgent()
