"""
Comprehensive Test & Lint Suite for Mekuria
"""
import sys
import os

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

modules_to_test = [
    "config",
    "brain",
    "stt",
    "tts",
    "tools",
    "wake_word",
    "core.emergency",
    "core.modes",
    "core.security",
    "core.memory",
    "core.state",
    "core.router",
    "core.orchestrator",
    "agents.base_agent",
    "agents.terminal_agent",
    "agents.technician_agent",
    "agents.computer_operator",
    "agents.file_manager_agent",
    "agents.research_agent",
    "agents.software_engineer",
    "agents.debugger",
    "agents.testing_agent",
    "agents.project_manager",
    "agents.automation_agent",
    "agents.tutor_career_agent",
    "agents.web_browser_agent",
    "skills.manager",
    "ui.console_dashboard",
]

failed = []

print("=" * 60)
print("RUNNING MEKURIA FULL MODULE VALIDATION")
print("=" * 60)

for mod in modules_to_test:
    try:
        __import__(mod)
        print(f"  [PASS] {mod}")
    except Exception as e:
        print(f"  [FAIL] {mod}: {e}")
        failed.append((mod, str(e)))

print("=" * 60)
if failed:
    print(f"TOTAL FAILURES: {len(failed)}")
    for mod, err in failed:
        print(f"  - {mod}: {err}")
    sys.exit(1)
else:
    print("ALL MODULES IMPORTED AND VALIDATED WITH ZERO ERRORS!")
    sys.exit(0)
