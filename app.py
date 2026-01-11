from flask import Flask, render_template, request, send_file
from utils.github_analyzer import analyze_repo
from utils.tech_stack_detector import detect_tech_stack
from utils.ai_suggester import get_ai_suggestions
from utils.project_intent_analyzer import analyze_project_intent
from utils.repo_readiness_checker import calculate_repo_readiness
from utils.pdf_report_generator import generate_pdf_report
import os

app = Flask(__name__)
app.secret_key = "dev-secret"


@app.route("/", methods=["GET", "POST"])
def home():
    repo_info = None
    tech_stack = None
    ai_suggestions = None
    project_intent_report = None
    readiness_report = None
    error_message = None
    files = []

    if request.method == "POST":
        repo_url = request.form.get("repo_url", "").strip()
        project_intent_text = request.form.get("project_intent", "").strip()

        if not repo_url:
            error_message = "Repository URL is empty."
        elif "github.com" not in repo_url:
            error_message = "Please enter a valid GitHub repository URL."
        else:
            try:
                repo_info, files = analyze_repo(repo_url)
                tech_stack = detect_tech_stack(files)

                ai_suggestions = get_ai_suggestions(repo_info, tech_stack)

                if project_intent_text:
                    project_intent_report = analyze_project_intent(
                        project_intent_text, files, tech_stack
                    )

                readiness_report = calculate_repo_readiness(
                    repo_info, files, tech_stack
                )

                # ✅ SAVE DATA FOR PDF DOWNLOAD
                app.last_analysis = {
                    "repo_info": repo_info,
                    "tech_stack": tech_stack,
                    "readiness_report": readiness_report,
                    "ai_suggestions": ai_suggestions
                }

            except Exception as e:
                print("ERROR:", e)
                error_message = "Unable to analyze this repository."

    return render_template(
        "index.html",
        repo_info=repo_info,
        tech_stack=tech_stack,
        ai_suggestions=ai_suggestions,
        project_intent_report=project_intent_report,
        readiness_report=readiness_report,
        error_message=error_message,
    )


# ✅ PDF DOWNLOAD ROUTE (THIS WAS MISSING OR MISPLACED)
@app.route("/download-pdf")
def download_pdf():
    if not hasattr(app, "last_analysis"):
        return "No analysis available. Analyze a repo first.", 400

    data = app.last_analysis
    file_path = "repo_analysis_report.pdf"

    generate_pdf_report(
        file_path=file_path,
        repo_info=data["repo_info"],
        tech_stack=data["tech_stack"],
        readiness_report=data["readiness_report"],
        ai_suggestions=data.get("ai_suggestions")
    )

    return send_file(file_path, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
