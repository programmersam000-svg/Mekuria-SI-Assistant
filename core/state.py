"""
╔══════════════════════════════════════════════════════════════╗
║           M E K U R I A   AI   A S S I S T A N T            ║
║              Task State & Recovery Checkpointer              ║
╚══════════════════════════════════════════════════════════════╝
Preserves long-running task states to disk. If Mekuria or a subtask
is interrupted, execution can be resumed seamlessly from the exact step.
"""

import os
import json
import datetime
from typing import Optional, Dict, Any, List

STATE_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "task_checkpoints.json")

class TaskStateRecovery:
    """Manages persistent checkpointing of complex goals and tasks."""

    @staticmethod
    def save_checkpoint(task_id: str, goal: str, steps: List[Dict[str, Any]], current_step_index: int, metadata: Dict[str, Any] = None):
        """Save active task state to disk."""
        data = TaskStateRecovery._load_all()
        data[task_id] = {
            "task_id": task_id,
            "goal": goal,
            "steps": steps,
            "current_step_index": current_step_index,
            "metadata": metadata or {},
            "status": "IN_PROGRESS",
            "updated_at": datetime.datetime.now().isoformat()
        }
        os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    @staticmethod
    def complete_task(task_id: str, result_summary: str):
        """Mark task as successfully finished."""
        data = TaskStateRecovery._load_all()
        if task_id in data:
            data[task_id]["status"] = "COMPLETED"
            data[task_id]["result_summary"] = result_summary
            data[task_id]["completed_at"] = datetime.datetime.now().isoformat()
            with open(STATE_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)

    @staticmethod
    def get_resumable_tasks() -> List[Dict[str, Any]]:
        """Retrieve any unfinished tasks for recovery."""
        data = TaskStateRecovery._load_all()
        return [t for t in data.values() if t.get("status") == "IN_PROGRESS"]

    @staticmethod
    def _load_all() -> Dict[str, Any]:
        if not os.path.exists(STATE_FILE):
            return {}
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}

task_recovery = TaskStateRecovery()
