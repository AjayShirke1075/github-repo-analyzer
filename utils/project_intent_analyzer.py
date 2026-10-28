"""
Project Intent vs Reality Analyzer
Compares stated developer intent against actual repository files, frameworks, and architecture.
"""

from utils.ai_engine import audit_intent_reality

def analyze_project_intent(intent_text, repo_files, tech_stack, repo_info=None, api_key=None, provider=None):
    repo_info = repo_info or {}
    return audit_intent_reality(
        intent_text=intent_text,
        repo_info=repo_info,
        tech_stack=tech_stack,
        files=repo_files,
        api_key=api_key,
        provider=provider
    )

__all__ = ["analyze_project_intent", "audit_intent_reality"]
