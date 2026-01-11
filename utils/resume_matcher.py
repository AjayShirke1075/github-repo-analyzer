def analyze_resume_fit(resume_text, tech_stack):
    # Normalize text
    resume_text = resume_text.lower()

    matched = []
    missing = []

    for tech in tech_stack:
        if tech.lower() in resume_text:
            matched.append(tech)
        else:
            missing.append(tech)

    if not tech_stack:
        score = 0
    else:
        score = int((len(matched) / len(tech_stack)) * 100)

    return {
        "score": score,
        "matched": matched,
        "missing": missing
    }
