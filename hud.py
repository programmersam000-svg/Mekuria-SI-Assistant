"""
╔══════════════════════════════════════════════════════════════╗
║           M E K U R I A   AI   A S S I S T A N T            ║
║              Live System HUD & Status Monitor                ║
╚══════════════════════════════════════════════════════════════╝
Holographic-style visual console dashboard showing live hardware telemetry,
active system clock, weather status, and Mekuria system readiness.
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
import tools

console = Console()


def make_layout() -> Layout:
    """Create the rich HUD layout grid."""
    layout = Layout()
    layout.split(
        Layout(name="header", size=4),
        Layout(name="body", ratio=1),
        Layout(name="footer", size=3),
    )
    layout["body"].split_row(
        Layout(name="system_stats", ratio=1),
        Layout(name="quick_commands", ratio=1),
    )
    return layout


def update_layout(layout: Layout):
    """Fetch live data and update layout panels."""
    now = datetime.now().strftime("%Y-%m-%d  %H:%M:%S")

    # Header
    layout["header"].update(
        Panel(
            Text(f"MEKURIA STARK-TECH HUD  |  {now}  |  STATUS: ONLINE", justify="center", style="bold cyan"),
            border_style="cyan",
        )
    )

    # Telemetry
    telemetry = tools.get_system_telemetry()

    stat_table = Table(title="Live Hardware Telemetry", expand=True, show_header=False)
    stat_table.add_column("Key", style="bold yellow")
    stat_table.add_column("Value", style="green")

    for line in telemetry.split(" | "):
        if ":" in line:
            k, v = line.split(":", 1)
            stat_table.add_row(k.strip(), v.strip())
        else:
            stat_table.add_row("Info", line.strip())

    layout["system_stats"].update(Panel(stat_table, border_style="green", title="Telemetry"))

    # Quick Commands & Tools
    cmd_table = Table(title="Active AI Tools & Actions", expand=True)
    cmd_table.add_column("Trigger", style="bold cyan")
    cmd_table.add_column("Action Description")

    cmd_table.add_row("Weather", "Get live weather & forecast")
    cmd_table.add_row("Wikipedia", "Summarize any topic")
    cmd_table.add_row("News", "Read top Google News headlines")
    cmd_table.add_row("Timer", "Set background voice alarm")
    cmd_table.add_row("Screenshot", "Save full screen to Desktop")
    cmd_table.add_row("YouTube", "Search and play music")
    cmd_table.add_row("Volume", "Set or mute master audio")

    layout["quick_commands"].update(Panel(cmd_table, border_style="magenta", title="Capabilities"))

    # Footer
    layout["footer"].update(
        Panel(
            Text(f"Voice Mode: {config.TTS_VOICE}  |  Brain: {config.LLM_MODEL}  |  Press Ctrl+C to exit HUD", justify="center", style="dim white"),
            border_style="cyan",
        )
    )


def run_hud():
    """Run the live updating HUD dashboard loop."""
    layout = make_layout()
    try:
        with Live(layout, refresh_per_second=1, screen=True):
            while True:
                update_layout(layout)
                time.sleep(1)
    except KeyboardInterrupt:
        console.print("[yellow]HUD Closed.[/yellow]")


if __name__ == "__main__":
    run_hud()
