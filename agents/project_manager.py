"""
╔══════════════════════════════════════════════════════════════╗
║           M E K U R I A   AI   A S S I S T A N T            ║
║              Project Manager & Task Tracker Agent            ║
╚══════════════════════════════════════════════════════════════╝
Tracks project completion percentages, task breakdowns, milestones,
dependencies, and TODO roadmaps across active projects.
"""

from typing import Dict, Any, List
from agents.base_agent import BaseAgent
from core.memory import memory

class ProjectManagerAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="ProjectManager",
            description="Manages project roadmaps, tracks progress %, dependencies, and task completion."
        )
        self._projects: Dict[str, Dict[str, Any]] = {}

    def create_project(self, project_name: str, goal: str, tasks: List[str]) -> Dict[str, Any]:
        """Create a new project tracking record."""
        self.log_step("Project Tracking", f"Registering project '{project_name}' with {len(tasks)} tasks...")
        proj_data = {
            "name": project_name,
            "goal": goal,
            "tasks": [{"title": t, "completed": False} for t in tasks],
            "progress": 0
        }
        self._projects[project_name] = proj_data
        return proj_data

    def mark_task_done(self, project_name: str, task_index: int) -> Dict[str, Any]:
        """Mark a specific task index as completed and recalculate percentage."""
        proj = self._projects.get(project_name)
        if proj and 0 <= task_index < len(proj["tasks"]):
            proj["tasks"][task_index]["completed"] = True
            done_count = sum(1 for t in proj["tasks"] if t["completed"])
            proj["progress"] = int((done_count / len(proj["tasks"])) * 100)
            self.log_step("Progress Update", f"{project_name}: {proj['progress']}% complete.")
            return proj
        return {"error": "Project or task index not found."}

    def get_status_report(self, project_name: str) -> str:
        """Format a clean project status summary."""
        proj = self._projects.get(project_name)
        if not proj:
            return f"No active record for project '{project_name}'."

        lines = [
            f"PROJECT: {proj['name']}",
            f"GOAL: {proj['goal']}",
            f"STATUS: {proj['progress']}%\n",
            "TASKS:"
        ]
        for t in proj["tasks"]:
            mark = "✓" if t["completed"] else "□"
            lines.append(f"  {mark} {t['title']}")
        return "\n".join(lines)

    def run(self, goal: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        name = context.get("project_name", "CurrentProject") if context else "CurrentProject"
        return {"report": self.get_status_report(name)}

project_manager = ProjectManagerAgent()
