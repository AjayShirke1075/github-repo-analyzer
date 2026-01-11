from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch


def generate_pdf_report(
    file_path,
    repo_info,
    tech_stack,
    readiness_report,
    ai_suggestions=None
):
    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4

    y = height - 50

    # Title
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, y, "GitHub Repository Analysis Report")
    y -= 40

    # Repo Info
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Repository Overview")
    y -= 20

    c.setFont("Helvetica", 10)
    c.drawString(50, y, f"Name: {repo_info.get('name')}")
    y -= 15
    c.drawString(50, y, f"Description: {repo_info.get('description')}")
    y -= 15
    c.drawString(50, y, f"Language: {repo_info.get('language')}")
    y -= 15
    c.drawString(50, y, f"Stars: {repo_info.get('stars')}")
    y -= 25

    # Tech Stack
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Detected Tech Stack")
    y -= 20

    c.setFont("Helvetica", 10)
    for tech in tech_stack:
        c.drawString(60, y, f"- {tech}")
        y -= 14

    y -= 10

    # Readiness
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Production Readiness")
    y -= 20

    c.setFont("Helvetica", 10)
    c.drawString(50, y, f"Score: {readiness_report['score']}%")
    y -= 15
    c.drawString(50, y, f"Badge: {readiness_report['badge']}")
    y -= 15

    for reason in readiness_report["reasons"]:
        c.drawString(60, y, f"- {reason}")
        y -= 14

    # AI Suggestions (optional)
    if ai_suggestions:
        y -= 20
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, "AI Suggestions")
        y -= 20

        c.setFont("Helvetica", 10)
        for line in ai_suggestions.split("\n"):
            c.drawString(60, y, line)
            y -= 14

    c.showPage()
    c.save()
