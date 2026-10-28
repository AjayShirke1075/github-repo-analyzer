"""
Repository Production Readiness Checker
Evaluates industry best practices, dependency hygiene, documentation,
test coverage indicators, and CI/CD automation across any programming language.
"""

from typing import Dict, List, Any


def calculate_repo_readiness(repo_info: Dict[str, Any], files: List[str], tech_stack: List[str]) -> Dict[str, Any]:
    score = 0
    reasons = []
    files_lower = [f.lower() for f in files]

    # 1. Documentation (20 pts)
    has_readme = any("readme" in f for f in files_lower)
    if has_readme:
        score += 20
        reasons.append("Comprehensive README documentation detected")
    else:
        reasons.append("README documentation is missing")

    # 2. Dependency Management (20 pts)
    dep_files = [
        "requirements.txt", "pyproject.toml", "pipfile", "package.json",
        "go.mod", "cargo.toml", "pom.xml", "build.gradle", "gemfile", "composer.json"
    ]
    has_deps = any(any(d in f for d in dep_files) for f in files_lower)
    if has_deps:
        score += 20
        reasons.append("Standard dependency manifest present (e.g. package.json, requirements.txt, go.mod)")
    else:
        reasons.append("No standard dependency manifest detected")

    # 3. Open Source License (15 pts)
    license_val = repo_info.get("license")
    if license_val and license_val != "No License":
        score += 15
        reasons.append(f"Valid Open Source License identified ({license_val})")
    else:
        reasons.append("No open source license found (limits legal adoption)")

    # 4. Automated Testing (20 pts)
    has_tests = any("test" in f or "spec" in f for f in files_lower)
    if has_tests:
        score += 20
        reasons.append("Automated testing suites and test fixtures detected")
    else:
        reasons.append("No automated test directory or test files detected")

    # 5. Environment & Git Hygiene (15 pts)
    has_gitignore = any(".gitignore" in f for f in files_lower)
    has_env = any(".env" in f or "config" in f for f in files_lower)
    if has_gitignore and has_env:
        score += 15
        reasons.append("Git hygiene & configuration templates present (.gitignore, config/.env)")
    elif has_gitignore or has_env:
        score += 10
        reasons.append("Partial environment configuration detected (.gitignore or config)")
    else:
        reasons.append("Missing .gitignore or environment configuration templates")

    # 6. CI/CD Bonus / Sanity (+10 pts bonus capped at 100)
    has_ci = any(".github" in f or "travis" in f or "circleci" in f or "jenkins" in f for f in files_lower)
    if has_ci:
        score += 10
        reasons.append("CI/CD pipeline automation detected (GitHub Actions / CI)")

    score = min(100, score)

    # Classification
    if score >= 85:
        badge = "🟢 Production Ready (Enterprise Tier)"
    elif score >= 70:
        badge = "🔵 High Quality (Candidate Portfolio Tier)"
    elif score >= 50:
        badge = "🟡 MVP / Demo Stage (Needs Hardening)"
    else:
        badge = "🔴 Early Prototype (Missing Key Engineering Foundations)"

    return {
        "score": score,
        "badge": badge,
        "reasons": reasons
    }
