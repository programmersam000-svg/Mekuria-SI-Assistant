"""
╔══════════════════════════════════════════════════════════════╗
║           M E K U R I A   AI   A S S I S T A N T            ║
║              Comprehensive System Test Suite                 ║
╚══════════════════════════════════════════════════════════════╝
Validates all 28 modules, core execution logic, memory persistence,
security policies, orchestrator planning, and tool operations.
"""

import sys
import os

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

print("=" * 65)
print("  MEKURIA ULTIMATE SYSTEM TEST & VALIDATION SUITE")
print("=" * 65)

passed = 0
failed = 0

def test_step(name, func):
    global passed, failed
    try:
        func()
        print(f"  [PASS] {name}")
        passed += 1
    except Exception as e:
        print(f"  [FAIL] {name}: {e}")
        failed += 1

# 1. Module Imports
modules = [
    "config", "brain", "stt", "tts", "tools", "wake_word",
    "core.emergency", "core.modes", "core.security", "core.memory",
    "core.state", "core.router", "core.orchestrator",
    "agents.base_agent", "agents.terminal_agent", "agents.technician_agent",
    "agents.computer_operator", "agents.file_manager_agent",
    "agents.research_agent", "agents.software_engineer", "agents.debugger",
    "agents.testing_agent", "agents.project_manager", "agents.automation_agent",
    "agents.tutor_career_agent", "agents.web_browser_agent",
    "skills.manager", "ui.console_dashboard"
]

print("\n--- 1. Module Import Tests ---")
for m in modules:
    test_step(f"Import {m}", lambda m=m: __import__(m))

print("\n--- 2. Core Subsystem Logic Tests ---")
def test_memory():
    from core.memory import memory
    memory.set_working("test_key", 12345)
    assert memory.get_working("test_key") == 12345
    memory.set_preference("theme", "dark_cyber")
    assert memory.get_preference("theme") == "dark_cyber"
test_step("Memory Working & SQLite Store", test_memory)

def test_security():
    from core.security import security
    masked = security.mask_secrets("My key is ghp_1234567890123456789012345678901234")
    assert "[PROTECTED_SECRET]" in masked
    assert security.is_dangerous_command("rm -rf /")
    assert not security.is_dangerous_command("python main.py")
test_step("Security Secret Masking & Risk Detection", test_security)

def test_modes():
    from core.modes import ModeManager, OperatingMode
    ModeManager.set_mode(OperatingMode.AGENT)
    assert ModeManager.is_autonomous()
    ModeManager.set_mode(OperatingMode.CHAT)
    assert ModeManager.is_chat_only()
    ModeManager.set_mode(OperatingMode.AGENT)
test_step("Operating Modes Controller", test_modes)

def test_tools():
    import tools
    t = tools.get_time_and_date()
    assert "time is" in t.lower()
    res = tools.calculate_math("sqrt(144) + 10")
    assert "22.0" in res or "22" in res
    j = tools.tell_joke()
    assert len(j) > 10
test_step("Built-in System Tools", test_tools)

def test_skills():
    from skills.manager import skill_manager
    skills = skill_manager.get_skills_list()
    assert "weather" in skills
    assert "calculator" in skills
test_step("Plugin & Skill System", test_skills)

def test_orchestrator():
    from core.orchestrator import orchestrator
    plan = orchestrator.understand_and_plan("Build a school management website")
    assert len(plan) >= 2
    assert any(p["agent"] == "software" for p in plan)
test_step("Orchestrator Goal Decomposition", test_orchestrator)

print("\n" + "=" * 65)
print(f"TEST RESULTS: {passed} PASSED | {failed} FAILED")
print("=" * 65)

if failed > 0:
    sys.exit(1)
else:
    print("ALL 34 TESTS AND SUB-MODULES PASSED WITH 100% SUCCESS!")
    sys.exit(0)
