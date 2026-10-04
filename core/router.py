"""
╔══════════════════════════════════════════════════════════════╗
║           M E K U R I A   AI   A S S I S T A N T            ║
║              Model Router & Cost Controller                  ║
╚══════════════════════════════════════════════════════════════╝
Routes queries to optimal models (Gemini Flash for speed/cost,
Gemini Pro/Reasoning for complex multi-step coding/planning) and tracks
token metrics.
"""

from typing import Dict, Any

class ModelRouter:
    """Intelligent model selection and usage tracking."""

    MODELS = {
        "fast": "gemini-2.5-flash",
        "reasoning": "gemini-2.5-pro",
        "coding": "gemini-2.5-flash",
        "vision": "gemini-2.5-flash",
    }

    _token_usage = {
        "prompt_tokens": 0,
        "completion_tokens": 0,
        "total_calls": 0,
    }

    @classmethod
    def select_model(cls, task_type: str = "general", complexity: str = "medium") -> str:
        """Select appropriate LLM model according to task type and complexity."""
        if complexity == "high" or task_type in ("deep_reasoning", "complex_refactor", "security_audit"):
            return cls.MODELS["reasoning"]
        return cls.MODELS["fast"]

    @classmethod
    def record_usage(cls, prompt_tokens: int = 0, completion_tokens: int = 0):
        cls._token_usage["prompt_tokens"] += prompt_tokens
        cls._token_usage["completion_tokens"] += completion_tokens
        cls._token_usage["total_calls"] += 1

    @classmethod
    def get_metrics(cls) -> Dict[str, Any]:
        return dict(cls._token_usage)

model_router = ModelRouter()
