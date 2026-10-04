"""
╔══════════════════════════════════════════════════════════════╗
║           M E K U R I A   AI   A S S I S T A N T            ║
║            Full Software Engineer & Developer Agent          ║
╚══════════════════════════════════════════════════════════════╝
Scaffolds projects (React, Next.js, FastAPI, Node, Python, Bots),
creates/modifies code files, installs dependencies, builds APIs,
and prepares production deployments.
"""

import os
import subprocess
from typing import Dict, Any, List
from agents.base_agent import BaseAgent
from core.security import security

class SoftwareEngineerAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="SoftwareEngineer",
            description="Builds web apps, backends, APIs, bots, mobile apps, and refactors code."
        )

    def write_code_file(self, file_path: str, code_content: str) -> str:
        """Create or update a code file safely."""
        self.log_step("Writing Code", f"Writing {len(code_content)} chars -> {file_path}")
        os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(code_content)
        security.audit_log(action="WriteCode", tool="SoftwareEngineer", status="SUCCESS", details=file_path)
        return f"File '{file_path}' written successfully."

    def scaffold_fastapi_project(self, target_dir: str) -> str:
        """Scaffold a production-ready Python FastAPI backend."""
        self.log_step("Scaffolding Project", f"Generating FastAPI project in '{target_dir}'...")
        os.makedirs(target_dir, exist_ok=True)

        main_py = (
            "from fastapi import FastAPI\n\n"
            "app = FastAPI(title='Mekuria API')\n\n"
            "@app.get('/')\n"
            "def read_root():\n"
            "    return {'status': 'online', 'system': 'Mekuria Autonomous Engine'}\n\n"
            "@app.get('/health')\n"
            "def health():\n"
            "    return {'health': 'ok'}\n"
        )
        reqs = "fastapi>=0.110.0\nuvicorn>=0.28.0\n"

        self.write_code_file(os.path.join(target_dir, "main.py"), main_py)
        self.write_code_file(os.path.join(target_dir, "requirements.txt"), reqs)
        return f"FastAPI project scaffolded at {target_dir}"

    def scaffold_html_landing(self, target_dir: str, title: str = "Modern Web App") -> str:
        """Scaffold a modern responsive HTML/Tailwind web page."""
        self.log_step("Scaffolding Web UI", f"Generating web UI in '{target_dir}'...")
        os.makedirs(target_dir, exist_ok=True)

        html_content = (
            "<!DOCTYPE html>\n<html lang='en'>\n<head>\n"
            f"  <meta charset='UTF-8'>\n  <meta name='viewport' content='width=device-width, initial-scale=1.0'>\n"
            f"  <title>{title}</title>\n"
            "  <script src='https://cdn.tailwindcss.com'></script>\n"
            "</head>\n<body class='bg-slate-900 text-white min-h-screen flex flex-col items-center justify-center p-6'>\n"
            "  <div class='max-w-2xl bg-slate-800 border border-slate-700 rounded-xl p-8 shadow-2xl text-center'>\n"
            f"    <h1 class='text-4xl font-extrabold text-cyan-400 mb-4'>{title}</h1>\n"
            "    <p class='text-slate-300 mb-6'>Built autonomously by Mekuria AI Operating Assistant.</p>\n"
            "    <button class='bg-cyan-500 hover:bg-cyan-600 text-slate-900 font-bold px-6 py-3 rounded-lg shadow transition'>Get Started</button>\n"
            "  </div>\n</body>\n</html>"
        )
        self.write_code_file(os.path.join(target_dir, "index.html"), html_content)
        return f"Web landing scaffolded at {target_dir}/index.html"

    def run(self, goal: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        lower = goal.lower()
        target = context.get("target_dir", "generated_app") if context else "generated_app"
        if "fastapi" in lower or "backend" in lower or "api" in lower:
            res = self.scaffold_fastapi_project(target)
        else:
            res = self.scaffold_html_landing(target, title=goal)
        return {"action": "scaffold", "result": res}

software_engineer = SoftwareEngineerAgent()
