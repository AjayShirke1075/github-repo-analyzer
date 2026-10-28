"""
AI Resume & Job Fit Matcher
Compares a candidate's resume or job description against the repository's tech stack and code evidence.
"""

from utils.ai_engine import match_resume_ai

def analyze_resume_fit(resume_text, tech_stack, repo_info=None, files=None, api_key=None, provider=None):
    repo_info = repo_info or {}
    files = files or []
    return match_resume_ai(
        resume_text=resume_text,
        repo_info=repo_info,
        tech_stack=tech_stack,
        files=files,
        api_key=api_key,
        provider=provider
    )

__all__ = ["analyze_resume_fit", "match_resume_ai"]
