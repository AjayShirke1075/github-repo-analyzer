from flask import Flask, render_template, request, send_file
import os

from utils.github_analyzer import analyze_repo
from utils.tech_stack_detector import detect_tech_stack
from utils.ai_suggester import get_ai_suggestions

from utils.project_intent_analyzer import analyze_project_intent
from utils.repo_readiness_checker import calculate_repo_readiness

from utils.flowchart_generator import (
    generate_structure_diagram,
    generate_dependency_flowchart,
    generate_how_it_works_diagram
)

app = Flask(__name__)
app.secret_key = "dev-secret"


@app.route("/", methods=["GET", "POST"])
def home():
    repo_info = None
    tech_stack = None
    ai_suggestions = None
    error_message = None

    project_intent_report = None
    readiness_report = None

    structure_diagram_path = None
    dependency_diagram_path = None
    how_it_works_diagram_path = None

    files = []

    if request.method == "POST":

        repo_url = request.form.get("repo_url", "").strip()
        project_intent_text = request.form.get("project_intent", "").strip()

        print("RECEIVED URL:", repr(repo_url))

        if not repo_url:
            error_message = "Repository URL is empty. Please paste the GitHub URL again."

        elif "github.com" not in repo_url:
            error_message = "Please enter a valid GitHub repository URL."

        else:
            try:
                # ✅ Analyze Repository
                repo_info, files = analyze_repo(repo_url)

                # ✅ Detect Tech Stack
                tech_stack = detect_tech_stack(files)

                # ✅ AI Suggestions (works only if API key has credits)
                ai_suggestions = get_ai_suggestions(repo_info, tech_stack)

                # ✅ Project Intent vs Reality (NO AI)
                if project_intent_text:
                    project_intent_report = analyze_project_intent(
                        project_intent_text,
                        files,
                        tech_stack
                    )

                # ✅ Repo Readiness Badge (NO AI)
                readiness_report = calculate_repo_readiness(
                    repo_info,
                    files,
                    tech_stack
                )

                # ✅ Structure Diagram
                try:
                    structure_diagram_path = generate_structure_diagram(repo_info["name"], files)
                except Exception as e:
                    print("STRUCTURE DIAGRAM ERROR:", e)
                    structure_diagram_path = None

                # ✅ Dependency Diagram
                try:
                    dependency_diagram_path = generate_dependency_flowchart(repo_info["name"], files)
                except Exception as e:
                    print("DEPENDENCY DIAGRAM ERROR:", e)
                    dependency_diagram_path = None

                # ✅ How Code Works Block Diagram
                try:
                    how_it_works_diagram_path = generate_how_it_works_diagram(repo_info["name"], tech_stack)
                except Exception as e:
                    print("HOW IT WORKS DIAGRAM ERROR:", e)
                    how_it_works_diagram_path = None

            except Exception as e:
                print("ERROR:", e)
                error_message = "Unable to analyze this repository. Please make sure it is public."

    return render_template(
        "index.html",
        repo_info=repo_info,
        tech_stack=tech_stack,
        ai_suggestions=ai_suggestions,
        error_message=error_message,

        project_intent_report=project_intent_report,
        readiness_report=readiness_report,

        structure_diagram_path=structure_diagram_path,
        dependency_diagram_path=dependency_diagram_path,
        how_it_works_diagram_path=how_it_works_diagram_path
    )


@app.route("/download-pdf")
def download_pdf():
    file_path = os.path.join("repo_analysis_report.pdf")
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return "PDF report not found!", 404


if __name__ == "__main__":
    app.run(debug=True)
