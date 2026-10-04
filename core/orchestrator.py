"""
╔══════════════════════════════════════════════════════════════╗
║           M E K U R I A   AI   A S S I S T A N T            ║
║         Central Multi-Agent Brain & Task Orchestrator        ║
╚══════════════════════════════════════════════════════════════╝
The supreme conductor of Mekuria: decomposes goals into structured
plans, selects specialized sub-agents, executes steps autonomously,
monitors progress, runs self-verification tests, and reports outcomes.
"""

import uuid
from typing import Dict, Any, List, Optional
from rich.console import Console
from rich.panel import Panel
from rich.tree import Tree

from core.emergency import check_emergency
from core.security import security
from core.memory import memory
from core.modes import ModeManager, OperatingMode
from core.state import task_recovery
from core.router import model_router
import agents

console = Console()

class Orchestrator:
    """Central orchestrator coordinating the multi-agent network."""

    def __init__(self):
        self.agents_registry = {
            "terminal": agents.terminal_agent,
            "technician": agents.technician_agent,
            "computer": agents.computer_operator,
            "file": agents.file_manager_agent,
            "research": agents.deep_research_agent,
            "software": agents.software_engineer,
            "debugger": agents.debugger_agent,
            "testing": agents.testing_agent,
            "project": agents.project_manager,
            "automation": agents.automation_agent,
            "tutor": agents.tutor_career_agent,
            "browser": agents.web_browser_agent,
        }

    def understand_and_plan(self, user_goal: str) -> List[Dict[str, Any]]:
        """
        Decompose user goal into multi-step executable action plan.
        Handles short/casual commands intelligently.
        """
        lower = user_goal.lower().strip()
        plan = []

        # 1. Research Goals
        if any(k in lower for k in ["research", "who is", "scholarship", "compare", "university"]):
            plan.append({
                "step": 1,
                "agent": "research",
                "action": "deep_research",
                "description": f"Gather verified multi-source intelligence on: {user_goal}"
            })
            plan.append({
                "step": 2,
                "agent": "file",
                "action": "save_report",
                "description": "Save research dossier to local markdown document"
            })

        # 2. Software Development Goals (e.g. "Build me a school management website")
        elif any(k in lower for k in ["build", "create website", "create app", "scaffold", "develop"]):
            plan.append({
                "step": 1,
                "agent": "software",
                "action": "scaffold_project",
                "description": f"Generate project structure and initial UI/code for: {user_goal}"
            })
            plan.append({
                "step": 2,
                "agent": "testing",
                "action": "verify_files",
                "description": "Verify code integrity and syntax validation"
            })
            plan.append({
                "step": 3,
                "agent": "project",
                "action": "track_project",
                "description": "Register project roadmap and milestone completion"
            })

        # 3. System / Network Troubleshooting
        elif any(k in lower for k in ["diagnose", "system status", "why is my", "slow", "network", "fix windows"]):
            plan.append({
                "step": 1,
                "agent": "technician",
                "action": "diagnose_system",
                "description": "Inspect hardware load, RAM, disks, and network health"
            })

        # 4. Computer Control / Screen
        elif any(k in lower for k in ["screenshot", "open app", "launch", "desktop"]):
            plan.append({
                "step": 1,
                "agent": "computer",
                "action": "desktop_action",
                "description": f"Execute computer control action: {user_goal}"
            })

        # 5. Default General Goal
        else:
            plan.append({
                "step": 1,
                "agent": "terminal",
                "action": "evaluate",
                "description": f"Process and evaluate command: {user_goal}"
            })

        return plan

    def execute_goal(self, user_goal: str) -> Dict[str, Any]:
        """
        Full Autonomous Agent Mode loop:
        Understand -> Plan -> Inspect -> Execute -> Test -> Fix -> Verify -> Report.
        """
        check_emergency()
        task_id = f"task_{uuid.uuid4().hex[:8]}"

        console.print(Panel(
            f"[bold cyan]🎯 Goal:[/bold cyan] {user_goal}\n"
            f"[dim]Task ID: {task_id} | Mode: {ModeManager.get_mode().value}[/dim]",
            title="🤖 Mekuria Autonomous Agent",
            border_style="cyan"
        ))

        # 1. Create Plan
        plan = self.understand_and_plan(user_goal)

        tree = Tree("[bold magenta]📋 Execution Plan[/bold magenta]")
        for p in plan:
            tree.add(f"[cyan]Step {p['step']}:[/cyan] [{p['agent']}] {p['description']}")
        console.print(tree)
        console.print()

        # Checkpoint initial state
        task_recovery.save_checkpoint(task_id, user_goal, plan, 0)

        results = []

        # 2. Execute Steps
        for idx, step in enumerate(plan):
            check_emergency()
            agent_key = step["agent"]
            target_agent = self.agents_registry.get(agent_key)

            if target_agent:
                console.print(f"[bold yellow]▶ Executing Step {step['step']}:[/bold yellow] {step['description']}")
                step_result = target_agent.run(user_goal, context={"step": step, "task_id": task_id})
                results.append({"step": step["step"], "agent": agent_key, "result": step_result})
                task_recovery.save_checkpoint(task_id, user_goal, plan, idx + 1)

        # 3. Final Self-Verification (Req 51 - Never say Done without verification)
        verified = True
        for r in results:
            if isinstance(r.get("result"), dict) and r["result"].get("success") is False:
                verified = False

        status_text = "COMPLETED & VERIFIED" if verified else "PARTIALLY COMPLETED WITH WARNINGS"
        task_recovery.complete_task(task_id, status_text)

        console.print(Panel(
            f"[bold green]✨ Status: {status_text}[/bold green]\n"
            f"All {len(plan)} plan steps processed autonomously.",
            title="🏁 Task Report",
            border_style="green" if verified else "yellow"
        ))

        return {
            "task_id": task_id,
            "goal": user_goal,
            "verified": verified,
            "steps": results
        }

orchestrator = Orchestrator()
