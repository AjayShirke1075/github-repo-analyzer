def calculate_repo_readiness(repo_info, files, tech_stack):
    score = 0
    reasons = []

    # README
    if any(f.lower() == "readme.md" for f in files):
        score += 20
        reasons.append("README.md present")
    else:
        reasons.append("README.md missing")

    # requirements.txt
    if "requirements.txt" in files:
        score += 20
        reasons.append("requirements.txt present")
    else:
        reasons.append("requirements.txt missing")

    # License
    if repo_info.get("license"):
        score += 15
        reasons.append("License present")
    else:
        reasons.append("License missing")

    # Tests
    if any("test" in f.lower() for f in files):
        score += 20
        reasons.append("Tests detected")
    else:
        reasons.append("No tests found")

    # Config / env
    if any(f.endswith(".env") or "config" in f.lower() for f in files):
        score += 15
        reasons.append("Configuration setup detected")
    else:
        reasons.append("No config/env setup")

    # Final badge
    if score >= 75:
        badge = "🟢 Production Ready"
    elif score >= 50:
        badge = "🔵 Internship Ready"
    elif score >= 30:
        badge = "🟡 Demo Ready"
    else:
        badge = "🔴 Not Ready"

    return {
        "score": score,
        "badge": badge,
        "reasons": reasons
    }
