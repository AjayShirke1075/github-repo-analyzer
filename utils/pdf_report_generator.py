"""
Professional PDF Report Generator for GitHub Repository Analysis
Built with ReportLab using dynamic flowables, tables, and multi-page layouts.
Robust XML entity escaping to guarantee flawless PDF compilation.
"""

import os
import re
import html
from typing import Dict, List, Any, Optional
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib.units import inch


def sanitize_for_pdf(text: str) -> str:
    """Escapes XML entities and converts markdown bold safely without invalid nesting."""
    if not text:
        return ""
    # Strip backticks to prevent courier nesting bugs
    text = text.replace("`", "")
    # Escape XML entities
    safe = html.escape(text)
    # Convert bold **text** to <b>text</b>
    safe = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', safe)
    # Strip any loose asterisks
    safe = safe.replace("*", "")
    # Balance <b> tags
    open_b = safe.count("<b>")
    close_b = safe.count("</b>")
    if open_b > close_b:
        safe += "</b>" * (open_b - close_b)
    elif close_b > open_b:
        for _ in range(close_b - open_b):
            idx = safe.rfind("</b>")
            if idx != -1:
                safe = safe[:idx] + safe[idx+4:]
    return safe


def generate_pdf_report(
    file_path: str,
    repo_info: Dict[str, Any],
    tech_stack: List[str],
    readiness_report: Dict[str, Any],
    ai_suggestions: Optional[str] = None,
    interview_qa: Optional[str] = None,
    intent_report: Optional[Dict[str, Any]] = None
) -> str:
    """
    Generates a comprehensive multi-page PDF report for the analyzed repository.
    """
    os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)

    doc = SimpleDocTemplate(
        file_path,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#1e3a8a"),
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        "DocSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#475569"),
        spaceAfter=12
    )

    section_heading = ParagraphStyle(
        "SectionHeading",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=17,
        textColor=colors.HexColor("#0f172a"),
        spaceBefore=14,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        "BodyDark",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#334155")
    )

    bullet_style = ParagraphStyle(
        "BulletText",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#334155"),
        leftIndent=14,
        spaceAfter=3
    )

    story = []

    # Title & Header
    story.append(Paragraph("⚡ GitHub Repository Analysis & AI Audit Report", title_style))
    repo_name = repo_info.get("name", "Repository")
    story.append(Paragraph(f"Comprehensive Engineering & Readiness Audit for <b>{sanitize_for_pdf(repo_name)}</b>", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#2563eb"), spaceAfter=12))

    # Section 1: Overview Table
    story.append(Paragraph("📊 Repository Overview", section_heading))
    overview_data = [
        [
            Paragraph("<b>Repository:</b>", body_style),
            Paragraph(sanitize_for_pdf(repo_info.get('name', 'N/A')), body_style),
            Paragraph("<b>Language:</b>", body_style),
            Paragraph(sanitize_for_pdf(repo_info.get('language') or 'N/A'), body_style),
        ],
        [
            Paragraph("<b>Stars:</b>", body_style),
            Paragraph(f"{repo_info.get('stars', 0):,}", body_style),
            Paragraph("<b>Forks:</b>", body_style),
            Paragraph(f"{repo_info.get('forks', 0):,}", body_style),
        ],
        [
            Paragraph("<b>Open Issues:</b>", body_style),
            Paragraph(f"{repo_info.get('open_issues', 0):,}", body_style),
            Paragraph("<b>Size:</b>", body_style),
            Paragraph(f"{repo_info.get('size', 0):,} KB", body_style),
        ],
        [
            Paragraph("<b>License:</b>", body_style),
            Paragraph(sanitize_for_pdf(repo_info.get('license', 'None')), body_style),
            Paragraph("<b>Updated:</b>", body_style),
            Paragraph(sanitize_for_pdf(repo_info.get('updated_at', 'N/A')), body_style),
        ],
    ]

    t_overview = Table(overview_data, colWidths=[1.1 * inch, 2.3 * inch, 1.1 * inch, 2.3 * inch])
    t_overview.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(t_overview)
    story.append(Spacer(1, 10))

    # Section 2: Production Readiness
    story.append(Paragraph("🚀 Production Readiness Evaluation", section_heading))
    score = readiness_report.get("score", 0)
    badge = readiness_report.get("badge", "Evaluation Complete")
    
    score_data = [
        [
            Paragraph(f"<b>Overall Score:</b> {score} / 100", body_style),
            Paragraph(f"<b>Classification:</b> {sanitize_for_pdf(badge)}", body_style)
        ]
    ]
    t_score = Table(score_data, colWidths=[3.4 * inch, 3.4 * inch])
    t_score.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#eff6ff")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#3b82f6")),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(t_score)
    story.append(Spacer(1, 6))

    for reason in readiness_report.get("reasons", []):
        story.append(Paragraph(f"• {sanitize_for_pdf(reason)}", bullet_style))
    story.append(Spacer(1, 10))

    # Section 3: Tech Stack
    if tech_stack:
        story.append(Paragraph("🛠️ Detected Technology Stack", section_heading))
        tech_text = ", ".join(tech_stack)
        story.append(Paragraph(f"<b>Identified Technologies:</b> {sanitize_for_pdf(tech_text)}", body_style))
        story.append(Spacer(1, 10))

    # Section 4: AI Architecture & Engineering Audit
    if ai_suggestions:
        story.append(Paragraph("🤖 AI Architectural & Code Quality Audit", section_heading))
        lines = ai_suggestions.split("\n")
        current_p = []
        for line in lines:
            line_str = line.strip()
            if not line_str:
                if current_p:
                    p_content = " ".join(current_p)
                    story.append(Paragraph(sanitize_for_pdf(p_content), body_style))
                    story.append(Spacer(1, 3))
                    current_p = []
            elif line_str.startswith("### ") or line_str.startswith("## ") or line_str.startswith("# "):
                if current_p:
                    story.append(Paragraph(sanitize_for_pdf(" ".join(current_p)), body_style))
                    current_p = []
                h_text = line_str.lstrip("#").strip()
                story.append(Paragraph(f"<b>{sanitize_for_pdf(h_text)}</b>", section_heading))
            elif line_str.startswith("- ") or line_str.startswith("* ") or line_str.startswith("• "):
                if current_p:
                    story.append(Paragraph(sanitize_for_pdf(" ".join(current_p)), body_style))
                    current_p = []
                b_text = line_str.lstrip("-*• ").strip()
                story.append(Paragraph(f"• {sanitize_for_pdf(b_text)}", bullet_style))
            else:
                current_p.append(line_str)

        if current_p:
            story.append(Paragraph(sanitize_for_pdf(" ".join(current_p)), body_style))
        story.append(Spacer(1, 10))

    # Section 5: Technical Interview Prep
    if interview_qa:
        story.append(Paragraph("🎯 Technical Interview Preparation & Model Q&A", section_heading))
        for line in interview_qa.split("\n"):
            line_str = line.strip()
            if line_str.startswith("#### ") or line_str.startswith("### "):
                story.append(Spacer(1, 6))
                story.append(Paragraph(f"<b>{sanitize_for_pdf(line_str.lstrip('#').strip())}</b>", section_heading))
            elif line_str.startswith("* ") or line_str.startswith("- ") or line_str.startswith("• "):
                clean_bullet = line_str.lstrip("*-• ").strip()
                story.append(Paragraph(f"• {sanitize_for_pdf(clean_bullet)}", bullet_style))
            elif line_str and not line_str.startswith("---"):
                story.append(Paragraph(sanitize_for_pdf(line_str), body_style))

    doc.build(story)
    return file_path
