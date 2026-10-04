"""
Mekuria Specialized Multi-Agent Network
"""

from agents.base_agent import BaseAgent
from agents.terminal_agent import terminal_agent
from agents.technician_agent import technician_agent
from agents.computer_operator import computer_operator
from agents.file_manager_agent import file_manager_agent
from agents.research_agent import deep_research_agent
from agents.software_engineer import software_engineer
from agents.debugger import debugger_agent
from agents.testing_agent import testing_agent
from agents.project_manager import project_manager
from agents.automation_agent import automation_agent
from agents.tutor_career_agent import tutor_career_agent
from agents.web_browser_agent import web_browser_agent

__all__ = [
    "BaseAgent",
    "terminal_agent",
    "technician_agent",
    "computer_operator",
    "file_manager_agent",
    "deep_research_agent",
    "software_engineer",
    "debugger_agent",
    "testing_agent",
    "project_manager",
    "automation_agent",
    "tutor_career_agent",
    "web_browser_agent",
]
