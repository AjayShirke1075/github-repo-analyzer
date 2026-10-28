"""
AI Code Reviewer compatibility wrapper.
Delegates to unified AI Engine supporting Google Gemini, OpenAI, and deterministic Static Heuristics.
"""

from utils.ai_engine import review_code_snippet

def review_code_file(filename, code, tech_stack, api_key=None, provider=None):
    res = review_code_snippet(filename, code, tech_stack, api_key=api_key, provider=provider)
    return res.get("content", "")

__all__ = ["review_code_file", "review_code_snippet"]
