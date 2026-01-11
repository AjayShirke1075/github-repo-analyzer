def analyze_project_intent(intent_text, repo_files, tech_stack):
    intent_text = intent_text.lower()
    repo_files_lower = [f.lower() for f in repo_files]

    report = {
        "matches": [],
        "warnings": [],
        "missing": []
    }

    # ---------- Flask / Backend ----------
    if "flask" in intent_text:
        if any("flask" in tech.lower() for tech in tech_stack):
            report["matches"].append("Flask framework detected in repository")
        else:
            report["missing"].append("Project claims Flask but Flask not detected")

    # ---------- Python ----------
    if "python" in intent_text:
        if any("python" in tech.lower() for tech in tech_stack):
            report["matches"].append("Python detected as main language")
        else:
            report["missing"].append("Project claims Python but Python not detected")

    # ---------- Documentation ----------
    if "student" in intent_text or "understand" in intent_text:
        if any("readme" in f for f in repo_files_lower):
            report["matches"].append("README found for documentation")
        else:
            report["warnings"].append("README missing or insufficient")

    # ---------- Testing ----------
    if "test" in intent_text or "quality" in intent_text:
        if any("test" in f for f in repo_files_lower):
            report["matches"].append("Test files detected")
        else:
            report["warnings"].append("No test files found")

    # ---------- API ----------
    if "api" in intent_text:
        if any("api" in f or "route" in f for f in repo_files_lower):
            report["matches"].append("API-related files detected")
        else:
            report["warnings"].append("No clear API structure found")

    return report
