"""
╔══════════════════════════════════════════════════════════════╗
║           M E K U R I A   AI   A S S I S T A N T            ║
║              Developer Console & Mission Control             ║
╚══════════════════════════════════════════════════════════════╝
Live mission control dashboard displaying:
  - Agent status & Multi-Agent Network
  - Hardware Telemetry (RAM, CPU, Disks)
  - Installed Skills & Plugins
  - Operating Mode & Security Level
  - In-flight Task Checkpoints
"""

import sys
import time
from datetime import datetime

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

import config
from core.modes import ModeManager
from core.state import task_recovery
from core.router import model_router
from skills.manager import skill_manager
import tools

console = Console()

def create_dashboard_layout() -> Layout:
    layout = Layout()
    layout.split(
        Layout(name="header", size=3),
        Layout(name="main", ratio=1),
        Layout(name="footer", size=3),
    )
    layout["main"].split_row(
        Layout(name="left", ratio=1),
        Layout(name="right", ratio=1),
    )
    layout["left"].split(
        Layout(name="telemetry", ratio=1),
        Layout(name="agents", ratio=1),
    )
    layout["right"].split(
        Layout(name="tasks", ratio=1),
        Layout(name="skills", ratio=1),
    )
    return layout

def update_dashboard_data(layout: Layout):
    now = datetime.now().strftime("%Y-%m-%d  %H:%M:%S")

    # Header
    layout["header"].update(
        Panel(
            Text(f"🛡️ MEKURIA MISSION CONTROL  |  {now}  |  MODE: {ModeManager.get_mode().value}  |  MODEL: {config.LLM_MODEL}", justify="center", style="bold cyan"),
            border_style="cyan",
        )
    )

    # 1. Telemetry
    telemetry = tools.get_system_telemetry()
    t_table = Table(title="Hardware & System Telemetry", expand=True, show_header=False)
    t_table.add_column("Property", style="bold yellow")
    t_table.add_column("Value", style="green")
    for item in telemetry.split(" | "):
        if ":" in item:
            k, v = item.split(":", 1)
            t_table.add_row(k.strip(), v.strip())
    layout["left"]["telemetry"].update(Panel(t_table, border_style="green", title="Telemetry"))

    # 2. Agent Status
    a_table = Table(title="Specialized Multi-Agent Network", expand=True)
    a_table.add_column("Agent", style="bold magenta")
    a_table.add_column("Role")
    a_table.add_column("Status", style="green")
    
    agent_list = [
        ("Orchestrator", "Central Planning & Goal Decomposition", "ONLINE"),
        ("TerminalAgent", "Safe Shell & Command Center", "READY"),
        ("TechnicianAgent", "Windows Diagnostics & Network", "READY"),
        ("ComputerOperator", "Screen Vision & Window Manager", "READY"),
        ("SoftwareEngineer", "Code Generation & Architecture", "READY"),
        ("DebuggerAgent", "Automated Root-Cause Patching", "READY"),
        ("DeepResearchAgent", "Multi-Source Fact Retrieval", "READY"),
        ("FileManagerAgent", "Document Intelligence & ZIP", "READY"),
        ("ProjectManager", "Task Roadmaps & Milestones", "READY"),
        ("TestingAgent", "Self-Verification & Test Suite", "READY"),
    ]
    for name, role, stat in agent_list:
        a_table.add_row(name, role, stat)
    layout["left"]["agents"].update(Panel(a_table, border_style="magenta", title="Agent Network"))

    # 3. Tasks
    tasks = task_recovery.get_resumable_tasks()
    task_table = Table(title="Active & Resumable Tasks", expand=True)
    task_table.add_column("Task ID", style="bold cyan")
    task_table.add_column("Goal")
    task_table.add_column("Status", style="yellow")
    if tasks:
        for t in tasks[:5]:
            task_table.add_row(t.get("task_id", ""), t.get("goal", "")[:30], t.get("status", ""))
    else:
        task_table.add_row("---", "No pending tasks in queue", "IDLE")
    layout["right"]["tasks"].update(Panel(task_table, border_style="yellow", title="Task Checkpoints"))

    # 4. Skills
    skills = skill_manager.get_skills_list()
    s_table = Table(title="Loaded Skills & Plugins", expand=True)
    s_table.add_column("Skill Name", style="bold cyan")
    s_table.add_column("Description")
    for s_name, desc in list(skills.items())[:6]:
        s_table.add_row(s_name, desc)
    layout["right"]["skills"].update(Panel(s_table, border_style="blue", title="Plugin Subsystem"))

    # Footer
    metrics = model_router.get_metrics()
    layout["footer"].update(
        Panel(
            Text(f"Total Model Calls: {metrics['total_calls']}  |  Emergency Stop: ARMED ('STOP MEKURIA')  |  Press Ctrl+C to exit", justify="center", style="dim white"),
            border_style="cyan",
        )
    )

def run_developer_console():
    """Launch Developer Console live dashboard."""
    layout = create_dashboard_layout()
    try:
        with Live(layout, refresh_per_second=1, screen=True):
            while True:
                update_dashboard_data(layout)
                time.sleep(1)
    except KeyboardInterrupt:
        console.print("[yellow]Developer Console exited.[/yellow]")

if __name__ == "__main__":
    run_developer_console()
