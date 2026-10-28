"""
AI Suggester compatibility wrapper.
Delegates to unified AI Engine supporting Google Gemini, OpenAI, and deterministic Smart Local Fallback.
"""

from utils.ai_engine import get_ai_suggestions

__all__ = ["get_ai_suggestions"]
