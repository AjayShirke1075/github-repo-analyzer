"""
GitHub Repository Analyzer & AI Developer Intelligence Platform
A production-grade Flask application featuring:
  - Multi-Provider AI Architecture & Code Audit (Gemini, OpenAI, Smart Local Engine)
  - Automated Entry File Discovery & Deep Code Review
  - Technical Interview Preparation & Model Q&A Generator
  - AI Project Intent vs Reality Auditor
  - AI Resume & Job Fit Matcher
  - Real Architecture & Workflow Flowcharts
  - Dynamic On-The-Fly PDF Report Generator
"""

import os
import json
from flask import Flask, render_template, request, send_file, jsonify, session

from utils.github_analyzer import analyze_repo, fetch_file_content
from utils.tech_stack_detector import detect_tech_stack
from utils.repo_readiness_checker import calculate_repo_readiness

from utils.ai_engine import (
    get_ai_suggestions,
    review_code_snippet,
    generate_interview_questions,
    audit_intent_reality,
    match_resume_ai
)

from utils.flowchart_generator import (
    generate_structure_diagram,
    generate_dependency_flowchart,
    generate_how_it_works_diagram
)

from utils.pdf_report_generator import generate_pdf_report

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret-key-ai-repo-analyzer-2026")

# In-memory store for the latest analysis to support dynamic PDF generation
LATEST_ANALYSIS_CACHE = {}


def find_primary_entry_file(files):
    """Identifies the most representative source code entrypoint in the repository."""
    priority = [
        "app.py", "main.py", "server.py", "run.py", "index.py", "wsgi.py",
        "src/index.js", "src/main.js", "src/App.js", "index.js", "server.js",
        "src/index.ts", "src/main.ts", "src/App.tsx",
        "main.go", "src/main.rs", "App.java"
    ]
    for p in priority:
        if p in files:
            return p
    for f in files:
        if any(f.endswith(ext) for ext in [".py", ".js", ".ts", ".go", ".rs", ".java"]) and not any(x in f for x in ["test", "vendor", "node_modules"]):
            return f
    return None


@app.route("/", methods=["GET", "POST"])
def home():
    repo_info = None
    tech_stack = None
    ai_suggestions = None
    ai_code_review = None
    interview_qa = None
    project_intent_report = None
    resume_report = None
    error_message = None

    structure_diagram_path = None
    dependency_diagram_path = None
    how_it_works_diagram_path = None

    repo_url = ""
    project_intent_text = ""
    resume_text = ""
    ai_provider = "auto"
    custom_api_key = ""
    github_token = ""

    if request.method == "POST":
        repo_url = request.form.get("repo_url", "").strip()
        project_intent_text = request.form.get("project_intent", "").strip()
        resume_text = request.form.get("resume_text", "").strip()
        ai_provider = request.form.get("ai_provider", "auto").strip()
        custom_api_key = request.form.get("api_key", "").strip()
        github_token = request.form.get("github_token", "").strip()

        if not repo_url:
            error_message = "Please enter a GitHub repository URL."
        elif "github.com" not in repo_url:
            error_message = "Please enter a valid GitHub repository URL (e.g., https://github.com/psf/requests)."
        else:
            try:
                # 1. Fetch Repository Metadata & File Tree
                repo_info, files, repo_obj = analyze_repo(repo_url, custom_token=github_token)

                # 2. Detect Technology Stack
                tech_stack = detect_tech_stack(files)

                # 3. Calculate Production Readiness
                readiness_report = calculate_repo_readiness(repo_info, files, tech_stack)

                # 4. Locate Primary Entry File & Read Sample Code
                entry_file = find_primary_entry_file(files)
                sample_code = ""
                if entry_file and repo_obj:
                    sample_code = fetch_file_content(repo_obj, entry_file, max_chars=4000)

                # 5. AI Architectural Suggestions
                ai_suggestions = get_ai_suggestions(
                    repo_info=repo_info,
                    tech_stack=tech_stack,
                    files=files,
                    sample_code=sample_code,
                    api_key=custom_api_key,
                    provider=ai_provider
                )

                # 6. AI Code & Security Review (File Level)
                if entry_file and sample_code:
                    ai_code_review = review_code_snippet(
                        filename=entry_file,
                        code_content=sample_code,
                        tech_stack=tech_stack,
                        api_key=custom_api_key,
                        provider=ai_provider
                    )

                # 7. AI Technical Interview Questions & Answers
                interview_qa = generate_interview_questions(
                    repo_info=repo_info,
                    tech_stack=tech_stack,
                    files=files,
                    api_key=custom_api_key,
                    provider=ai_provider
                )

                # 8. AI Project Intent vs Reality Auditor
                if project_intent_text:
                    project_intent_report = audit_intent_reality(
                        intent_text=project_intent_text,
                        repo_info=repo_info,
                        tech_stack=tech_stack,
                        files=files,
                        api_key=custom_api_key,
                        provider=ai_provider
                    )

                # 9. AI Resume & Job Fit Matcher
                if resume_text:
                    resume_report = match_resume_ai(
                        resume_text=resume_text,
                        repo_info=repo_info,
                        tech_stack=tech_stack,
                        files=files,
                        api_key=custom_api_key,
                        provider=ai_provider
                    )

                # 10. Visual Architecture & Flowchart Diagrams
                try:
                    structure_diagram_path = generate_structure_diagram(repo_info["name"], files)
                except Exception as e:
                    print(f"[Diagram Error] Structure: {e}")

                try:
                    dependency_diagram_path = generate_dependency_flowchart(repo_info["name"], files)
                except Exception as e:
                    print(f"[Diagram Error] Dependency: {e}")

                try:
                    how_it_works_diagram_path = generate_how_it_works_diagram(repo_info["name"], tech_stack)
                except Exception as e:
                    print(f"[Diagram Error] How-it-works: {e}")

                # 11. Cache Results for Dynamic PDF Export and AI Chat Assistant
                LATEST_ANALYSIS_CACHE["current"] = {
                    "repo_info": repo_info,
                    "tech_stack": tech_stack,
                    "readiness_report": readiness_report,
                    "ai_suggestions": ai_suggestions.get("content") if ai_suggestions else None,
                    "interview_qa": interview_qa.get("content") if interview_qa else None,
                    "intent_report": project_intent_report,
                    "files": files,
                    "sample_code": sample_code,
                    "entry_file": entry_file,
                    "api_key": custom_api_key,
                    "ai_provider": ai_provider
                }

            except ValueError as ve:
                error_message = str(ve)
            except Exception as e:
                print(f"[General Error] {e}")
                error_message = f"Analysis error: {str(e)}"

    return render_template(
        "index.html",
        repo_info=repo_info,
        tech_stack=tech_stack,
        readiness_report=readiness_report if repo_info else None,
        ai_suggestions=ai_suggestions,
        ai_code_review=ai_code_review,
        interview_qa=interview_qa,
        project_intent_report=project_intent_report,
        resume_report=resume_report,
        structure_diagram_path=structure_diagram_path,
        dependency_diagram_path=dependency_diagram_path,
        how_it_works_diagram_path=how_it_works_diagram_path,
        error_message=error_message,
        repo_url=repo_url,
        project_intent_text=project_intent_text,
        resume_text=resume_text,
        ai_provider=ai_provider,
        custom_api_key=custom_api_key
    )


@app.route("/download-pdf")
def download_pdf():
    """Generates and serves a customized, multi-page PDF report for the active analysis."""
    analysis = LATEST_ANALYSIS_CACHE.get("current")
    if not analysis or not analysis.get("repo_info"):
        return "No repository has been analyzed yet. Please analyze a repository first.", 400

    pdf_output_path = os.path.join("static", "reports", "repo_analysis_report.pdf")
    try:
        generate_pdf_report(
            file_path=pdf_output_path,
            repo_info=analysis["repo_info"],
            tech_stack=analysis["tech_stack"],
            readiness_report=analysis["readiness_report"],
            ai_suggestions=analysis.get("ai_suggestions"),
            interview_qa=analysis.get("interview_qa"),
            intent_report=analysis.get("intent_report")
        )
        safe_name = analysis["repo_info"]["name"].replace("/", "_")
        return send_file(
            pdf_output_path,
            as_attachment=True,
            download_name=f"{safe_name}_AI_Audit_Report.pdf"
        )
    except Exception as e:
        print(f"[PDF Export Error] {e}")
        return f"Failed to generate PDF: {str(e)}", 500


@app.route("/api/ask", methods=["POST"])
def ask_repo_ai():
    """Interactive AI Assistant: Answers questions about the current repository."""
    data = request.get_json() or {}
    question = data.get("question", "").strip()
    api_key_override = data.get("api_key", "").strip()
    provider_override = data.get("provider", "").strip()
    chat_history = data.get("history", [])

    analysis = LATEST_ANALYSIS_CACHE.get("current")

    if not question:
        return jsonify({"error": "Empty question provided."}), 400

    if not analysis or not analysis.get("repo_info"):
        return jsonify({"error": "No active repository analyzed yet. Please run an analysis first."}), 400

    from utils.ai_engine import answer_codebase_chat

    # Resolve active API key and provider
    active_key = api_key_override or analysis.get("api_key")
    active_provider = provider_override or analysis.get("ai_provider") or "auto"

    res = answer_codebase_chat(
        question=question,
        repo_info=analysis["repo_info"],
        tech_stack=analysis.get("tech_stack", []),
        files=analysis.get("files", []),
        sample_code=analysis.get("sample_code", ""),
        readiness_report=analysis.get("readiness_report", {}),
        chat_history=chat_history,
        api_key=active_key,
        provider=active_provider
    )

    return jsonify({
        "answer": res.get("answer", "No answer generated."),
        "source": res.get("source", "AI Assistant")
    })


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
