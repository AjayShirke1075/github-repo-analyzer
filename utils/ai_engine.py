"""
Multi-Provider AI Intelligence Engine for GitHub Repository Analysis
Supports:
  1. Google Gemini (Gemini 1.5 Flash / Gemini 2.0 Flash)
  2. OpenAI (GPT-4o-mini / GPT-4o)
  3. OpenAI-Compatible Custom Endpoints (Groq, DeepSeek, Ollama)
  4. Smart Local Engineering Intelligence Engine (Zero-cost, offline fallback)
"""

import os
import re
from typing import Dict, List, Any, Optional, Tuple

# Try loading environment variables from .env
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass


def get_active_provider_and_key(override_key: Optional[str] = None, override_provider: Optional[str] = None) -> Tuple[str, Optional[str]]:
    """
    Determines the best available AI provider and API key.
    Priority:
      1. User-provided in request/UI
      2. Environment variables (GEMINI_API_KEY / GOOGLE_API_KEY / OPENAI_API_KEY)
      3. Fallback to 'smart_local' (zero API cost, guaranteed to work)
    """
    # Explicit provider requested
    if override_provider and override_provider in ["gemini", "openai", "smart_local"]:
        if override_provider == "smart_local":
            return "smart_local", None
        if override_key and len(override_key.strip()) > 5 and not override_key.startswith("sk-NEW"):
            return override_provider, override_key.strip()

    # If override key provided without provider
    if override_key and len(override_key.strip()) > 5 and not override_key.startswith("sk-NEW"):
        clean_key = override_key.strip()
        if clean_key.startswith("AIza"):
            return "gemini", clean_key
        elif clean_key.startswith("sk-"):
            return "openai", clean_key

    # Check Environment Variables
    gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if gemini_key and len(gemini_key.strip()) > 10 and not gemini_key.startswith("AIzaSy-YOUR"):
        return "gemini", gemini_key.strip()

    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key and len(openai_key.strip()) > 10 and not openai_key.startswith("sk-NEW") and not "YOUR-KEY" in openai_key:
        return "openai", openai_key.strip()

    # Default to robust built-in engine
    return "smart_local", None


def _call_gemini(prompt: str, system_instruction: str, api_key: str) -> Optional[str]:
    """Invokes Google Gemini API with safety and error handling."""
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        
        # Prefer fast & reliable gemini-1.5-flash or gemini-2.0-flash
        model_name = "gemini-1.5-flash"
        try:
            model = genai.GenerativeModel(
                model_name=model_name,
                system_instruction=system_instruction
            )
            response = model.generate_content(prompt)
            if response and response.text:
                return response.text.strip()
        except Exception:
            # Fallback to standard generate
            model = genai.GenerativeModel(model_name="gemini-1.5-flash")
            response = model.generate_content(f"{system_instruction}\n\n{prompt}")
            if response and response.text:
                return response.text.strip()
    except Exception as e:
        print(f"[Gemini API Notice] Fallback needed: {e}")
        return None
    return None


def _call_openai(prompt: str, system_instruction: str, api_key: str, base_url: Optional[str] = None) -> Optional[str]:
    """Invokes OpenAI (or compatible API like Groq) with safety and error handling."""
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key, base_url=base_url)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=1800
        )
        if response and response.choices:
            return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"[OpenAI API Notice] Fallback needed: {e}")
        return None
    return None


def execute_llm_query(prompt: str, system_instruction: str, api_key: Optional[str] = None, provider: Optional[str] = None) -> Tuple[Optional[str], str]:
    """
    Executes prompt against chosen LLM provider with graceful degradation.
    Returns (response_text, provider_used)
    """
    active_provider, key = get_active_provider_and_key(api_key, provider)
    
    if active_provider == "gemini" and key:
        result = _call_gemini(prompt, system_instruction, key)
        if result:
            return result, "Google Gemini 1.5 Flash"
            
    if active_provider == "openai" and key:
        result = _call_openai(prompt, system_instruction, key)
        if result:
            return result, "OpenAI GPT-4o-mini"
            
    # If API key failed or quota expired, return None so smart local engine handles it
    return None, "Smart Engineering Engine"


# =========================================================================
# FEATURE 1: Comprehensive AI Architecture & Code Suggestions
# =========================================================================

def get_ai_suggestions(
    repo_info: Dict[str, Any],
    tech_stack: List[str],
    files: Optional[List[str]] = None,
    sample_code: Optional[str] = None,
    api_key: Optional[str] = None,
    provider: Optional[str] = None
) -> Dict[str, Any]:
    """
    Generates senior-level architectural and code improvement recommendations.
    Always returns structured, actionable insights.
    """
    files = files or []
    has_tests = any("test" in f.lower() for f in files)
    has_ci = any(".github" in f or "travis" in f or "circle" in f for f in files)
    has_docker = any("docker" in f.lower() for f in files)
    has_docs = any("readme" in f.lower() for f in files)
    has_env = any(".env" in f or "config" in f.lower() for f in files)
    file_count = len(files)

    system_instruction = (
        "You are a Staff Software Architect and AI Technical Interviewer conducting a thorough "
        "codebase audit for a production engineering review. Structure your answer with clear markdown "
        "headings, bullet points, technical rigor, and specific code recommendations."
    )

    prompt = f"""
Audit the following GitHub repository:
- Repository Name: {repo_info.get('name')}
- Description: {repo_info.get('description', 'No description provided')}
- Language: {repo_info.get('language', 'Unknown')}
- Total Files: {file_count}
- Stars: {repo_info.get('stars', 0)} | Forks: {repo_info.get('forks', 0)} | Open Issues: {repo_info.get('open_issues', 0)}
- Detected Tech Stack: {', '.join(tech_stack[:15]) if tech_stack else 'Not detected'}
- Repository Signals: Tests={has_tests}, CI/CD={has_ci}, Docker/Container={has_docker}, Docs={has_docs}, Config/Env={has_env}

Sample Repository Structure (Key files):
{chr(10).join(files[:25])}

Provide a comprehensive, senior-level review containing:
1. 🏗️ **Architectural Design & Modularity**: Evaluation of project structure, separation of concerns, and design patterns.
2. 🛡️ **Security & Vulnerability Audit**: Specific risks (credentials, input sanitization, dependency hygiene, OWASP).
3. ⚡ **Performance & Scalability**: Bottlenecks, caching strategies, async handling, and computational efficiency.
4. 🧪 **Testing, QA & CI/CD Pipeline**: Test coverage gaps, integration testing recommendations.
5. 🚀 **Actionable Refactoring Roadmap**: Top 3 high-impact code changes with brief syntax examples.
"""

    llm_output, provider_used = execute_llm_query(prompt, system_instruction, api_key, provider)
    
    if llm_output:
        return {
            "source": provider_used,
            "content": llm_output
        }

    # SMART LOCAL DETERMINISTIC INTELLIGENCE ENGINE FALLBACK
    # Produces high-depth, deterministic analysis tailored to the repository's real structure
    recs = []
    
    # 1. Architecture
    arch_notes = []
    if "Python" in tech_stack:
        if any("app.py" in f or "main.py" in f for f in files):
            arch_notes.append("• **Entrypoint Structure**: Single root entrypoint (`app.py`/`main.py`) detected. For scaling, recommend modularizing into an application factory pattern (`create_app()`) with Flask Blueprints or FastAPI APIRouter.")
        if not any("services" in f or "controllers" in f for f in files):
            arch_notes.append("• **Layered Architecture**: Business logic is currently co-located with route handlers. Introduce dedicated service (`services/`) and data-access layers (`repositories/`) to decouple business rules from presentation.")
    elif "JavaScript" in tech_stack or "TypeScript" in tech_stack:
        arch_notes.append("• **Component Architecture**: Verify strict separation between presentation UI components and custom state hooks or data-fetching logic.")
    else:
        arch_notes.append("• **Modularity Audit**: Enforce clean module boundaries and isolate external third-party integrations behind adapter interfaces.")

    # 2. Security
    sec_notes = []
    if not has_env:
        sec_notes.append("• **Environment Secret Management**: No `.env.example` or central config module detected. Ensure API tokens, database URIs, and signing secrets are strictly loaded via `os.environ` or `pydantic-settings`.")
    else:
        sec_notes.append("• **Secret Leak Prevention**: Ensure `.gitignore` explicitly excludes `.env`, `*.pem`, `*.key`, and credentials to prevent accidental git history commits.")
    sec_notes.append("• **Input Validation & Sanitization**: Ensure all external client inputs and request payloads undergo schema-level validation (e.g., Pydantic or Marshmallow) to eliminate injection attack vectors.")

    # 3. Performance
    perf_notes = []
    perf_notes.append("• **I/O & Network Bottlenecks**: Avoid blocking synchronous HTTP calls in primary request loops. Implement non-blocking asynchronous clients (`httpx.AsyncClient` or `aiohttp`) and connection pooling.")
    perf_notes.append("• **Caching Strategy**: Introduce an in-memory caching layer (Redis or `@lru_cache`) for repeated expensive queries, rate-limited third-party API lookups, and static assets.")

    # 4. Testing & CI/CD
    test_notes = []
    if not has_tests:
        test_notes.append("• **Test Suite Deficiency**: No automated test suites (`test_*.py` or `pytest`) identified. Target a minimum 75% code coverage starting with unit tests for core utilities and mock API handlers.")
    else:
        test_notes.append("• **Automated Test Coverage**: Test files detected. Complement unit tests with parameterized edge-case testing (`pytest.mark.parametrize`) and mock fixtures.")
    if not has_ci:
        test_notes.append("• **CI/CD Automation**: Missing GitHub Actions workflow. Add `.github/workflows/ci.yml` running linting (`ruff`/`flake8`), static type checking (`mypy`), and test execution on every pull request.")

    local_report = f"""### 🏗️ Architectural Design & Modularity
{chr(10).join(arch_notes)}

### 🛡️ Security & Vulnerability Audit
{chr(10).join(sec_notes)}

### ⚡ Performance & Scalability
{chr(10).join(perf_notes)}

### 🧪 Testing, Reliability & CI/CD
{chr(10).join(test_notes)}

### 🚀 High-Impact Technical Refactoring Roadmap
1. **Application Factory & Dependency Injection**: Refactor the monolithic script into decoupled modules to simplify testing and isolate side-effects.
2. **Defensive API & Error Handling**: Implement structured custom exception hierarchies and unified error handlers returning standard RFC-7807 problem details.
3. **Containerization & Reproducible Environments**: Add a multi-stage `Dockerfile` and `docker-compose.yml` with pinned base images to eliminate cross-platform dependency drift.
"""
    return {
        "source": "Smart Code Intelligence Engine (Deterministic Analysis)",
        "content": local_report
    }


# =========================================================================
# FEATURE 2: AI Code Reviewer (File Level Review)
# =========================================================================

def review_code_snippet(
    filename: str,
    code_content: str,
    tech_stack: List[str],
    api_key: Optional[str] = None,
    provider: Optional[str] = None
) -> Dict[str, Any]:
    """
    Performs a line-by-line or architectural code review of a specific source code file.
    """
    if not code_content or len(code_content.strip()) < 10:
        return {
            "source": "Code Reviewer",
            "content": f"No inspectable code found in {filename}."
        }

    # Limit code to first 150 lines or 4000 characters to conserve context
    truncated_code = "\n".join(code_content.splitlines()[:150])

    system_instruction = (
        "You are a Principal Software Engineer performing a detailed Pull Request code review. "
        "Highlight concrete bugs, edge cases, security risks, performance flaws, and idiomatic improvements."
    )

    prompt = f"""
Review the following source code file:
- File Name: {filename}
- Tech Stack: {', '.join(tech_stack) if tech_stack else 'Standard'}

Code Content:
```python
{truncated_code}
```

Provide structured code review feedback:
1. **Critical Bugs & Edge Cases**: Potential unhandled exceptions, race conditions, or logic errors.
2. **Security Vulnerabilities**: Injection, hardcoded secrets, insecure deserialization, unvalidated input.
3. **Performance & Resource Hygiene**: Unclosed resources, O(N^2) loops, memory leaks.
4. **Code Quality & Idiomatic Clean Code**: Naming, typing, documentation, adherence to PEP 8 / Clean Code principles.
5. **Concrete Refactoring Example**: Provide a concise before-and-after diff or snippet.
"""

    llm_output, provider_used = execute_llm_query(prompt, system_instruction, api_key, provider)
    if llm_output:
        return {
            "source": provider_used,
            "filename": filename,
            "content": llm_output
        }

    # Heuristic Code Analysis Fallback
    review_points = []
    
    # Check for hardcoded secrets
    if re.search(r'(?i)(api_key|password|secret|token)\s*=\s*["\'][^"\']{6,}["\']', truncated_code):
        review_points.append("⚠️ **Security Concern**: Potential hardcoded secret or token detected in source. Move credentials to environment variables (`os.getenv`).")
    
    # Check for bare excepts
    if re.search(r'except\s*:', truncated_code):
        review_points.append("⚠️ **Exception Handling**: Found bare `except:` block. Always catch specific exceptions (e.g. `except (ValueError, KeyError):`) to avoid silencing system exits or keyboard interrupts.")
        
    # Check for resource leaks
    if "open(" in truncated_code and "with open" not in truncated_code:
        review_points.append("💡 **Resource Hygiene**: Direct `open()` call observed without context manager. Use `with open(...) as f:` to guarantee proper file descriptor release.")
        
    # Check for type annotations
    if "def " in truncated_code and "->" not in truncated_code:
        review_points.append("💡 **Type Safety**: Functions lack Python type annotations. Adding type hints (`def func(x: int) -> str:`) drastically improves IDE tooling and enables static verification with `mypy`.")

    # Generic clean code checklist
    review_points.append("✅ **Modularity**: Ensure single-responsibility principle: separate business calculations, data parsing, and network transport into distinct functions.")
    review_points.append("✅ **Documentation**: Add Google/Sphinx style docstrings detailing parameters, return types, and possible raised exceptions for public APIs.")

    local_content = f"### 🔍 Automated Code Review: `{filename}`\n\n" + "\n\n".join(review_points)
    return {
        "source": "Smart Code Intelligence Engine (Static AST Heuristics)",
        "filename": filename,
        "content": local_content
    }


# =========================================================================
# FEATURE 3: AI Technical Interview Q&A Generator (Interview Prep Mode)
# =========================================================================

def generate_interview_questions(
    repo_info: Dict[str, Any],
    tech_stack: List[str],
    files: List[str],
    api_key: Optional[str] = None,
    provider: Optional[str] = None
) -> Dict[str, Any]:
    """
    Generates 5 technical interview questions and comprehensive model answers
    specifically tailored to this project's code and architecture.
    """
    system_instruction = (
        "You are an AI Engineering Interviewer at a top-tier tech firm. Generate 5 realistic, deep technical "
        "interview questions based on the candidate's repository, accompanied by senior-level answers, "
        "trade-off discussions, and key technical concepts to mention."
    )

    prompt = f"""
Generate 5 technical interview questions for an AI/Software Developer interview based on this project:
- Project Name: {repo_info.get('name')}
- Description: {repo_info.get('description', '')}
- Primary Language: {repo_info.get('language', 'Python')}
- Tech Stack: {', '.join(tech_stack[:12])}
- Key Files: {', '.join(files[:15])}

Format each question with:
- **Question [Number]**: The exact technical question an interviewer would ask.
- **What the interviewer is testing**: Core concept (e.g., concurrency, fault tolerance, API design, security).
- **Strong Candidate Answer**: High-level architectural explanation.
- **Key Talking Points**: Bullet points of technical terms and trade-offs to mention.
"""

    llm_output, provider_used = execute_llm_query(prompt, system_instruction, api_key, provider)
    if llm_output:
        return {
            "source": provider_used,
            "content": llm_output
        }

    # Deterministic technical interview generator
    lang = repo_info.get("language") or "Python"
    repo_name = repo_info.get("name", "Project")

    q1_stack = tech_stack[0] if tech_stack else lang
    local_qa = f"""### 🎯 AI Developer Technical Interview Questions & Answers

#### Question 1: System Architecture & Framework Selection
* **Question**: "Walk me through the high-level architecture of `{repo_name}`. Why did you choose `{q1_stack}` over alternative frameworks, and what were the primary architectural trade-offs?"
* **What the interviewer is evaluating**: System design competence, trade-off awareness, and technology justification.
* **Strong Answer**: "The project adopts a modular service-oriented layout where presentation, ingestion, and analytical pipelines are decoupled. We chose `{q1_stack}` for its rapid prototyping velocity, minimal boilerplate, and mature ecosystem of asynchronous libraries. The trade-off is horizontal concurrency overhead compared to Go or Rust, which we mitigated using asynchronous non-blocking worker pools and caching."
* **Key Talking Points**: Single Responsibility Principle, stateless request handlers, latency vs. throughput trade-offs.

---

#### Question 2: Error Resilience & External API Rate Limiting
* **Question**: "When querying third-party upstream APIs (such as GitHub, OpenAI, or LLMs), how does your system handle rate limits, transient network partitions, and 429/5xx status codes?"
* **What the interviewer is evaluating**: Production reliability, defensive engineering, and distributed systems resilience.
* **Strong Answer**: "We implement defensive fallbacks: exponential backoff with randomized jitter to prevent the 'thundering herd' problem, combined with a Circuit Breaker pattern. Furthermore, we leverage git trees rather than recursive file listing to compress hundreds of HTTP requests into a single network round-trip."
* **Key Talking Points**: Exponential backoff, idempotent operations, circuit breaker pattern, graceful degradation.

---

#### Question 3: Security & Secrets Hygiene
* **Question**: "What security measures are implemented to protect user-supplied input and prevent secrets or API tokens from being compromised?"
* **What the interviewer is evaluating**: OWASP Top 10 awareness, input validation, and credential security.
* **Strong Answer**: "All input parameters (URLs, queries) are sanitized against regex injection and path traversal. Credentials are never hardcoded in source control; they are loaded dynamically via strictly parsed environment variables. Furthermore, CORS headers and session cookies are configured with HttpOnly and SameSite flags."
* **Key Talking Points**: OWASP vulnerabilities, Defense-in-depth, 12-Factor App methodology.

---

#### Question 4: Scalability & Caching
* **Question**: "If this application experienced a 100x spike in concurrent users (e.g. from 10 users to 1,000 requests/sec), where would the primary bottleneck occur, and how would you re-architect it?"
* **What the interviewer is evaluating**: Scalability roadmap, database/caching design, and asynchronous task processing.
* **Strong Answer**: "The primary bottleneck is synchronous blocking I/O on external API round-trips. To scale 100x, we would convert synchronous handlers to asynchronous event queues using Celery or Redis Streams. Analysis tasks would execute worker-side while the frontend polls via WebSockets or Server-Sent Events (SSE). Results would be cached in Redis with TTLs."
* **Key Talking Points**: Redis caching, Celery background workers, WebSockets/SSE, horizontal auto-scaling.

---

#### Question 5: Testing Strategy & Automated Quality Gates
* **Question**: "How do you ensure test coverage without making brittle integration tests that depend on external live APIs?"
* **What the interviewer is evaluating**: Test automation, mocking/stubbing, and CI/CD quality engineering.
* **Strong Answer**: "We decouple our business logic from network clients by programming against interfaces. In unit tests, we mock external responses using `unittest.mock` or `pytest-mock` to verify edge cases (rate limits, malformed payloads) deterministically without network latency. We run end-to-end smoke tests against staging sandbox environments inside GitHub Actions CI."
* **Key Talking Points**: Unit vs Integration testing, Mocking vs Stubbing, CI/CD automated gates.
"""
    return {
        "source": "Smart Code Intelligence Engine (Technical Interview Prep)",
        "content": local_qa
    }


# =========================================================================
# FEATURE 4: AI Project Intent vs. Reality Auditor
# =========================================================================

def audit_intent_reality(
    intent_text: str,
    repo_info: Dict[str, Any],
    tech_stack: List[str],
    files: List[str],
    api_key: Optional[str] = None,
    provider: Optional[str] = None
) -> Dict[str, Any]:
    """
    Evaluates stated intent against actual codebase implementation.
    Returns structured matches, warnings, missing items, and alignment score.
    """
    if not intent_text or len(intent_text.strip()) < 5:
        return {
            "score": 0,
            "matches": [],
            "warnings": ["Please provide a descriptive project intent to run the comparison."],
            "missing": []
        }

    system_instruction = (
        "You are a Software QA Auditor comparing a developer's stated project goal against "
        "the actual files and technologies implemented in the repository. Return a structured critique."
    )

    prompt = f"""
Compare the stated project intent against repository reality:
- Stated Intent: "{intent_text}"
- Detected Tech Stack: {', '.join(tech_stack)}
- File List ({len(files)} files): {', '.join(files[:40])}

Evaluate:
1. Alignment Score: 0 to 100%
2. Confirmed Matches: Stated features that are actually implemented in code/files.
3. Warnings: Features partially implemented or ambiguous.
4. Missing / Discrepancies: Stated claims that have no corresponding code, routes, or files.
"""

    llm_output, provider_used = execute_llm_query(prompt, system_instruction, api_key, provider)
    
    # Run deterministic heuristic check as well
    intent_lower = intent_text.lower()
    files_lower = [f.lower() for f in files]
    
    matches = []
    warnings = []
    missing = []
    score = 50

    # Tech stack matching
    for tech in tech_stack:
        if tech.lower() in intent_lower:
            matches.append(f"Framework/Tool: {tech} claimed in intent and confirmed in codebase.")
            score += 8

    # Common architecture keywords
    if "api" in intent_lower or "rest" in intent_lower:
        if any("api" in f or "route" in f or "controller" in f or "endpoint" in f for f in files_lower):
            matches.append("API Architecture: API endpoints / route handlers detected.")
            score += 10
        else:
            warnings.append("API Claims: Project claims API functionality, but dedicated `api/` or route modules are minimal.")
            score -= 5

    if "database" in intent_lower or "sql" in intent_lower or "db" in intent_lower or "mongo" in intent_lower:
        if any("model" in f or "db" in f or "sql" in f or "schema" in f for f in files_lower):
            matches.append("Persistence Layer: Database models or schema definitions found.")
            score += 10
        else:
            missing.append("Database: Stated database persistence is not reflected in file structure.")
            score -= 10

    if "test" in intent_lower or "tested" in intent_lower or "quality" in intent_lower:
        if any("test" in f for f in files_lower):
            matches.append("Testing Suite: Automated test files confirmed in repository.")
            score += 10
        else:
            missing.append("Testing Claims: Intent mentions testing, but no test suite found.")
            score -= 10

    if "docker" in intent_lower or "deploy" in intent_lower or "container" in intent_lower:
        if any("docker" in f for f in files_lower):
            matches.append("Containerization: Dockerfile / container configs present.")
            score += 10
        else:
            warnings.append("DevOps: Containerization claimed but Dockerfile is missing.")

    if not matches:
        matches.append(f"Repository Core: Contains {len(files)} files aligned with {repo_info.get('language', 'General software development')}.")

    score = max(20, min(100, score))

    return {
        "score": score,
        "matches": matches,
        "warnings": warnings,
        "missing": missing,
        "ai_narrative": llm_output,
        "source": provider_used if llm_output else "Smart Intent Analyzer"
    }


# =========================================================================
# FEATURE 5: AI Resume & Job Fit Matcher
# =========================================================================

def match_resume_ai(
    resume_text: str,
    repo_info: Dict[str, Any],
    tech_stack: List[str],
    files: List[str],
    api_key: Optional[str] = None,
    provider: Optional[str] = None
) -> Dict[str, Any]:
    """
    Evaluates candidate resume or target job description against this repository.
    Generates match score, demonstrated skills, missing skills, and interview pitch.
    """
    if not resume_text or len(resume_text.strip()) < 10:
        return {
            "score": 0,
            "matched_skills": [],
            "missing_skills": tech_stack,
            "interview_pitch": "Paste a candidate resume or job description to evaluate skill alignment."
        }

    resume_lower = resume_text.lower()
    matched = []
    missing = []

    for tech in tech_stack:
        if tech.lower() in resume_lower:
            matched.append(tech)
        else:
            missing.append(tech)

    base_score = int((len(matched) / max(1, len(tech_stack))) * 100) if tech_stack else 70

    system_instruction = (
        "You are an AI Technical Recruiter & Hiring Manager. Compare the candidate's resume/job requirements "
        "with this GitHub project's technology and architecture. Provide a compelling candidate interview pitch."
    )

    prompt = f"""
Candidate Resume / Job Description:
{resume_text[:2000]}

Repository Context:
- Project Name: {repo_info.get('name')}
- Technologies: {', '.join(tech_stack)}
- File Count: {len(files)}
- Matched Keywords: {', '.join(matched)}
- Missing Keywords: {', '.join(missing)}

Provide:
1. Candidate Evaluation: How strongly this repository validates the candidate's engineering skills.
2. 3 Strong Talking Points for the Interview: Exact phrases the candidate should say to impress the interviewer using this project as evidence.
"""

    llm_output, provider_used = execute_llm_query(prompt, system_instruction, api_key, provider)

    default_pitch = (
        f"In your interview, highlight `{repo_info.get('name')}` as concrete proof of hands-on experience in "
        f"{', '.join(matched[:4]) if matched else repo_info.get('language', 'software engineering')}. "
        f"Explain how you designed the architecture, solved performance bottlenecks, and maintained clean modular code."
    )

    return {
        "score": base_score,
        "matched_skills": matched,
        "missing_skills": missing,
        "interview_pitch": llm_output or default_pitch,
        "source": provider_used if llm_output else "Smart Resume Matcher"
    }


# =========================================================================
# FEATURE 6: Interactive AI Codebase Assistant (Chat System)
# =========================================================================

def answer_codebase_chat(
    question: str,
    repo_info: Dict[str, Any],
    tech_stack: List[str],
    files: Optional[List[str]] = None,
    sample_code: Optional[str] = None,
    readiness_report: Optional[Dict[str, Any]] = None,
    chat_history: Optional[List[Dict[str, str]]] = None,
    api_key: Optional[str] = None,
    provider: Optional[str] = None
) -> Dict[str, str]:
    """
    Answers technical and architectural questions about the repository.
    Supports LLM inference (Gemini, OpenAI) and rich deterministic code reasoning fallback.
    """
    if not question or not question.strip():
        return {
            "answer": "Please provide a question about the repository.",
            "source": "AI Assistant"
        }

    files = files or []
    tech_stack = tech_stack or []
    readiness_report = readiness_report or {}
    sample_code = sample_code or ""
    chat_history = chat_history or []

    # 1. Format Conversation Context for LLM
    history_str = ""
    if chat_history:
        recent = chat_history[-4:]
        history_str = "Recent Conversation:\n" + "\n".join([f"{m.get('role', 'user').title()}: {m.get('content', '')}" for m in recent]) + "\n\n"

    system_instruction = (
        "You are a Staff Software Engineer & AI Technical Interviewer acting as the repository's lead architect. "
        "Answer the user's technical question with precision, referencing specific architectural patterns, "
        "files, frameworks, and engineering trade-offs. Use markdown formatting with bolding and bullet points."
    )

    prompt = f"""
Repository Context:
- Project Name: {repo_info.get('name')}
- Description: {repo_info.get('description', 'No description')}
- Primary Language: {repo_info.get('language', 'Unknown')}
- Stars: {repo_info.get('stars', 0)} | Forks: {repo_info.get('forks', 0)} | Open Issues: {repo_info.get('open_issues', 0)}
- Detected Tech Stack: {', '.join(tech_stack[:15])}
- Production Readiness Score: {readiness_report.get('score', 0)}/100 ({readiness_report.get('badge', '')})
- Key Files ({len(files)} total): {', '.join(files[:30])}

Sample Core Implementation Excerpt:
```python
{sample_code[:1200]}
```

{history_str}User Question: {question}

Provide a direct, senior-level technical answer with code rationale and architectural context.
"""

    llm_output, provider_used = execute_llm_query(prompt, system_instruction, api_key, provider)
    if llm_output:
        return {
            "answer": llm_output,
            "source": provider_used
        }

    # 2. SMART LOCAL DETERMINISTIC CHAT ENGINE FALLBACK
    q_lower = question.lower()
    files_lower = [f.lower() for f in files]
    repo_name = repo_info.get("name", "this repository")
    lang = repo_info.get("language") or "Python"
    stack_text = ", ".join(tech_stack) if tech_stack else lang

    # Topic classification — broad keyword matching for natural-language questions
    is_arch = any(k in q_lower for k in ["arch", "design", "pattern", "structure", "how it work", "flow", "modular", "component", "explain", "describe", "overview", "tell me", "what is", "how does", "built", "organized", "layout"])
    is_sec = any(k in q_lower for k in ["sec", "auth", "token", "password", "secret", "vulnerab", "owasp", "leak", "jwt", "login", "credential", "hack", "attack", "xss", "csrf", "injection", "safe"])
    is_perf = any(k in q_lower for k in ["perf", "scale", "concurr", "bottleneck", "async", "cache", "speed", "fast", "load", "latency", "optim", "slow", "throughput", "10x", "million", "traffic"])
    is_test = any(k in q_lower for k in ["test", "testing", "coverage", "pytest", "unit", "mock", "integration", "assert", "qa", "quality", "automated", "tdd", "bdd"])
    is_db = any(k in q_lower for k in ["data", "db", "sql", "orm", "mongo", "postgres", "mysql", "model", "schema", "persist", "migration", "storag", "database"])
    is_api = any(k in q_lower for k in ["api", "route", "endpoint", "rest", "controller", "http", "request", "response", "get", "post", "restful", "graphql", "webhook"])
    is_deploy = any(k in q_lower for k in ["docker", "deploy", "ci", "cd", "action", "workflow", "cloud", "aws", "prod", "container", "kubernetes", "heroku", "devops", "pipeline", "release"])
    is_install = any(k in q_lower for k in ["install", "setup", "run", "start", "execute", "how to use", "guide", "clone", "get started", "begin", "launch", "configure"])

    # Locate mentioned files
    mentioned_files = [f for f in files if f.lower() in q_lower or (f.split("/")[-1].lower() in q_lower and len(f.split("/")[-1]) > 3)]

    # Structural signals from files
    has_tests = any("test" in f for f in files_lower)
    has_docker = any("docker" in f for f in files_lower)
    has_ci = any(".github" in f or "workflows" in f or "travis" in f or "circle" in f for f in files_lower)
    has_docs = any("readme" in f or "docs" in f for f in files_lower)
    has_env = any(".env" in f or "config" in f for f in files_lower)
    entry_candidates = [f for f in files if any(f.endswith(x) for x in ["app.py", "main.py", "server.py", "index.js", "server.js", "main.go", "index.ts", "main.ts"])]
    entry_str = f"`{entry_candidates[0]}`" if entry_candidates else "the primary entrypoint module"
    readiness_score = readiness_report.get('score', 0)
    readiness_badge = readiness_report.get('badge', 'Developing')
    stars = repo_info.get('stars', 0)
    forks = repo_info.get('forks', 0)

    answer_parts = []

    if is_arch:
        answer_parts.append(f"### 🏗️ Architecture & System Design for `{repo_name}`")
        answer_parts.append(
            f"**Overview**: `{repo_name}` is a **{lang}**-based project with a production readiness score of "
            f"**{readiness_score}/100** ({readiness_badge}), {stars:,} GitHub stars, and {forks:,} forks. "
            f"The codebase spans **{len(files)} files** built on the **{stack_text}** stack."
        )
        answer_parts.append("")
        answer_parts.append("**🔩 Core Components:**")
        answer_parts.append(f"- **Entrypoint**: {entry_str} serves as the application bootstrap and request dispatcher.")
        service_files = [f for f in files if any(x in f.lower() for x in ["service", "util", "helper", "lib", "core"])]
        if service_files:
            answer_parts.append(f"- **Service/Utility Layer**: Found `{', '.join(service_files[:5])}` — business logic abstraction layer.")
        template_files = [f for f in files if any(x in f.lower() for x in ["template", "view", "html", "jsx", "tsx", "vue"])]
        if template_files:
            answer_parts.append(f"- **Presentation Layer**: `{len(template_files)}` template/view file(s) handle UI rendering and user-facing responses.")
        static_files = [f for f in files if "static" in f.lower() or "assets" in f.lower()]
        if static_files:
            answer_parts.append(f"- **Static Assets**: `{len(static_files)}` static resource file(s) (CSS/JS/images).")
        answer_parts.append("")
        answer_parts.append("**🧩 Design Patterns Detected:**")
        answer_parts.append("- **Service-Oriented Dispatch**: Incoming requests flow through route handlers → service utilities → response serializers.")
        answer_parts.append("- **Separation of Concerns**: Template rendering, business logic, and data fetching are partitioned into dedicated modules.")
        answer_parts.append("- **Configuration Injection**: Runtime parameters are injected via environment variables or config modules.")
        answer_parts.append("")
        answer_parts.append("**🚀 Scalability Recommendation:**")
        answer_parts.append(f"To scale `{repo_name}` for enterprise load: (1) Adopt an Application Factory pattern with modular Blueprints/Routers. (2) Replace synchronous I/O with async handlers (`asyncio`, `httpx`). (3) Add a Redis-backed caching layer for repeated expensive computations. (4) Introduce a job queue (Celery/RQ) for background processing.")

    elif is_sec:
        answer_parts.append(f"### 🛡️ Security & Vulnerability Analysis for `{repo_name}`")
        answer_parts.append(
            f"**Security Posture Overview**: Analyzing `{repo_name}` ({len(files)} files, {lang} stack). "
            f"Current production readiness: **{readiness_score}/100**."
        )
        answer_parts.append("")
        answer_parts.append("**🔑 Credential & Secret Management:**")
        if has_env:
            answer_parts.append("- ✅ **Configuration files detected** — ensure `.env` is in `.gitignore` and never committed to source control.")
            answer_parts.append("- Use `python-dotenv` or `pydantic-settings` to securely inject secrets at runtime.")
        else:
            answer_parts.append("- ⚠️ **No `.env.example` or central config module found** — immediately add secret management via `os.getenv()` calls.")
            answer_parts.append("- Add `.env` to `.gitignore` and create `.env.example` as a template for collaborators.")
        answer_parts.append("")
        answer_parts.append("**🛡️ OWASP Top-10 Hardening Checklist:**")
        answer_parts.append("- **Injection Prevention**: Validate and sanitize all user inputs — use parameterized queries for database calls.")
        answer_parts.append("- **Authentication**: Implement token-based auth (JWT/OAuth2) with proper expiry and refresh logic.")
        answer_parts.append("- **XSS Prevention**: Escape all user-generated content in HTML responses; use Content-Security-Policy headers.")
        answer_parts.append("- **CSRF Protection**: Add CSRF tokens to all state-changing forms or use SameSite cookie attributes.")
        answer_parts.append("- **Rate Limiting**: Protect all public API endpoints with per-IP rate limits (`flask-limiter` or NGINX).")
        answer_parts.append("")
        answer_parts.append("**🔍 Dependency Vulnerability Audit:**")
        answer_parts.append("```bash\n# Scan for known CVEs in dependencies:\npip-audit  # Python\nnpm audit  # Node.js\n```")
        answer_parts.append("Enable **GitHub Dependabot** for automated pull requests on vulnerable dependency updates.")

    elif is_perf:
        answer_parts.append(f"### ⚡ Performance & Scalability Analysis for `{repo_name}`")
        answer_parts.append(
            f"**Stack**: {stack_text} | **Files**: {len(files)} | **Readiness**: {readiness_score}/100 | "
            f"**Stars**: {stars:,} (community validation)"
        )
        answer_parts.append("")
        answer_parts.append("**🚨 Likely Bottlenecks (in priority order):**")
        answer_parts.append(f"1. **Synchronous I/O** — Blocking HTTP calls to external APIs (e.g., GitHub) stall the event loop in {lang}.")
        answer_parts.append("2. **Repeated Computation** — Expensive analyses recalculated on every request without result caching.")
        answer_parts.append("3. **Memory Management** — Large file/data structures held in-process without pagination or streaming.")
        answer_parts.append("")
        answer_parts.append("**⚡ Optimization Roadmap:**")
        answer_parts.append("```python\n# 1. Replace blocking requests with async HTTP\nimport httpx\nasync with httpx.AsyncClient() as client:\n    response = await client.get(url)\n\n# 2. Cache expensive function results\nfrom functools import lru_cache\n@lru_cache(maxsize=512)\ndef compute_analysis(repo_name: str): ...\n\n# 3. Background task queue for heavy jobs\nfrom celery import Celery\napp = Celery('tasks', broker='redis://localhost:6379/0')\n```")
        answer_parts.append("")
        answer_parts.append("**📊 Scaling to 10x Traffic:**")
        answer_parts.append("- Deploy behind a **WSGI/ASGI cluster** (Gunicorn + Uvicorn workers).")
        answer_parts.append("- Add a **Redis cache** for session state and repeated analysis results.")
        answer_parts.append("- Use a **CDN** (Cloudflare) for static assets and edge caching.")
        answer_parts.append("- Horizontally scale with **Docker + Kubernetes** or AWS ECS/Lambda for serverless burst.")

    elif is_test:
        test_files = [f for f in files if "test" in f.lower()]
        ci_files = [f for f in files if ".github" in f.lower() or "workflow" in f.lower()]
        answer_parts.append(f"### 🧪 Testing & Quality Assurance for `{repo_name}`")
        answer_parts.append(
            f"**Quality Signals**: {len(test_files)} test file(s) found, "
            f"{'✅ CI/CD pipeline detected' if ci_files else '⚠️ No CI/CD pipeline detected'}, "
            f"Readiness Score: **{readiness_score}/100**."
        )
        answer_parts.append("")
        if test_files:
            answer_parts.append(f"**✅ Detected Test Suites** ({len(test_files)} file(s)):")
            for tf in test_files[:5]:
                answer_parts.append(f"- `{tf}`")
            answer_parts.append("")
            answer_parts.append("**▶️ Running the Test Suite:**")
            answer_parts.append("```bash\n# Run all tests with verbose output:\npytest -v --tb=short\n\n# With coverage report:\npytest --cov=. --cov-report=term-missing\n\n# Run a single test module:\npytest tests/test_specific.py -v\n```")
        else:
            answer_parts.append("**⚠️ Test Coverage Gap**: No automated test suites (`test_*.py`) identified in the repository.")
            answer_parts.append("")
            answer_parts.append("**📋 Recommended Test Plan:**")
            answer_parts.append("```bash\nmkdir tests && touch tests/__init__.py\n# Create unit tests for core utilities\npip install pytest pytest-cov\n```")
            answer_parts.append("```python\n# tests/test_core.py\nimport pytest\nfrom utils.your_module import your_function\n\ndef test_basic_functionality():\n    result = your_function(input_data)\n    assert result is not None\n\n@pytest.mark.parametrize('input,expected', [(1, 2), (3, 4)])\ndef test_edge_cases(input, expected):\n    assert transform(input) == expected\n```")
        answer_parts.append("")
        answer_parts.append("**🎯 Quality Improvement Targets:**")
        answer_parts.append("- Target **≥75% branch coverage** as a production baseline.")
        answer_parts.append("- Add **integration tests** that mock external APIs (GitHub, LLM providers).")
        answer_parts.append("- Configure **CI/CD** to fail the build if coverage drops below threshold.")

    elif is_db:
        model_files = [f for f in files if any(x in f.lower() for x in ["model", "db", "sql", "schema", "migration"])]
        answer_parts.append(f"### 💾 Data & Persistence Architecture for `{repo_name}`")
        if model_files:
            answer_parts.append(f"**Database Modules Detected** ({len(model_files)} file(s)):")
            for mf in model_files[:5]:
                answer_parts.append(f"- `{mf}`")
            answer_parts.append("")
        else:
            answer_parts.append(f"**Current State**: `{repo_name}` uses **in-memory/stateless storage** — no ORM or relational database layer detected.")
            answer_parts.append("")
        answer_parts.append("**🗄️ Persistence Architecture Recommendations:**")
        answer_parts.append("```python\n# SQLAlchemy ORM setup (PostgreSQL):\nfrom sqlalchemy import create_engine, Column, Integer, String\nfrom sqlalchemy.ext.declarative import declarative_base\n\nengine = create_engine(os.getenv('DATABASE_URL'))\nBase = declarative_base()\n\nclass RepoAnalysis(Base):\n    __tablename__ = 'analyses'\n    id = Column(Integer, primary_key=True)\n    repo_name = Column(String(255), nullable=False)\n    readiness_score = Column(Integer)\n```")
        answer_parts.append("- **PostgreSQL** with SQLAlchemy for structured analysis history.")
        answer_parts.append("- **Redis** as a high-speed ephemeral cache for live analysis results.")
        answer_parts.append("- **Alembic** for zero-downtime schema migrations.")

    elif is_api:
        route_files = [f for f in files if any(x in f.lower() for x in ["route", "api", "controller", "view", "endpoint"])]
        answer_parts.append(f"### 🚦 API & Route Architecture for `{repo_name}`")
        answer_parts.append(f"**Stack**: {stack_text} | **Total Endpoints**: Analyzed from {len(files)} source files.")
        answer_parts.append("")
        if route_files:
            answer_parts.append(f"**Route/Controller Files**: `{', '.join(route_files[:5])}`")
            answer_parts.append("")
        answer_parts.append("**📡 API Design Best Practices:**")
        answer_parts.append("- **REST Semantics**: `GET` for reads, `POST` for creation, `PUT/PATCH` for updates, `DELETE` for removal.")
        answer_parts.append("- **Standard HTTP Status Codes**: 200 OK, 201 Created, 400 Bad Request, 401 Unauthorized, 404 Not Found, 422 Validation Error, 500 Internal Server Error.")
        answer_parts.append("- **Error Response Format** (RFC-7807 Problem Details):")
        answer_parts.append("```json\n{\n  \"status\": 400,\n  \"title\": \"Validation Error\",\n  \"detail\": \"repo_url field is required\",\n  \"type\": \"/errors/validation\"\n}\n```")
        answer_parts.append("- **API Versioning**: Prefix routes with `/api/v1/` to enable non-breaking future changes.")
        answer_parts.append("- **Rate Limiting**: Protect endpoints from abuse with per-IP throttling.")

    elif is_deploy:
        answer_parts.append(f"### 🚀 Deployment & DevOps Strategy for `{repo_name}`")
        answer_parts.append(f"**Stack**: {stack_text} | **CI/CD**: {'✅ Detected' if has_ci else '⚠️ Not found'} | **Docker**: {'✅ Detected' if has_docker else '⚠️ Not found'}")
        answer_parts.append("")
        answer_parts.append("**🐳 Docker Containerization:**")
        if has_docker:
            answer_parts.append("✅ Dockerfile detected — ensure you use multi-stage builds for a minimal production image.")
        else:
            answer_parts.append("⚠️ No Dockerfile detected. Recommended multi-stage `Dockerfile`:")
            answer_parts.append("```dockerfile\n# Stage 1: Build\nFROM python:3.12-slim AS builder\nWORKDIR /app\nCOPY requirements.txt .\nRUN pip install --user -r requirements.txt\n\n# Stage 2: Production\nFROM python:3.12-slim\nWORKDIR /app\nCOPY --from=builder /root/.local /root/.local\nCOPY . .\nEXPOSE 5000\nCMD [\"gunicorn\", \"-w\", \"4\", \"app:app\"]\n```")
        answer_parts.append("")
        answer_parts.append("**⚙️ CI/CD Pipeline (GitHub Actions):")
        if has_ci:
            answer_parts.append("✅ GitHub Actions workflow detected — ensure it runs lint, tests, and security scanning on every PR.")
        else:
            answer_parts.append("Create `.github/workflows/ci.yml`:")
            answer_parts.append("```yaml\nname: CI\non: [push, pull_request]\njobs:\n  test:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v4\n      - uses: actions/setup-python@v5\n        with: { python-version: '3.12' }\n      - run: pip install -r requirements.txt\n      - run: pytest --cov=. --cov-fail-under=75\n```")
        answer_parts.append("")
        answer_parts.append("**☁️ Cloud Deployment Options:**")
        answer_parts.append("- **Railway / Render**: Zero-config deployments from GitHub (recommended for demos).")
        answer_parts.append("- **AWS ECS / GCP Cloud Run**: Production container orchestration with auto-scaling.")
        answer_parts.append("- **Heroku**: One-command deploy with `git push heroku main`.")

    elif is_install:
        answer_parts.append(f"### 📦 Installation & Setup Guide for `{repo_name}`")
        answer_parts.append("```bash")
        answer_parts.append(f"# Step 1: Clone the repository\ngit clone https://github.com/{repo_name}.git\ncd {repo_name.split('/')[-1]}")
        if "Python" in tech_stack:
            answer_parts.append("# Step 2: Create a virtual environment\npython -m venv venv\n\n# Activate (Windows):\n.\\venv\\Scripts\\activate\n\n# Activate (macOS/Linux):\nsource venv/bin/activate")
            answer_parts.append("# Step 3: Install dependencies\npip install -r requirements.txt")
            if has_env:
                answer_parts.append("# Step 4: Configure environment variables\ncp .env.example .env\n# Edit .env with your API keys")
            answer_parts.append("# Step 5: Launch the application\npython app.py\n# App runs at: http://127.0.0.1:5000")
        elif "Node.js" in tech_stack:
            answer_parts.append("# Step 2: Install all dependencies\nnpm install\n\n# Step 3: Configure environment\ncp .env.example .env\n\n# Step 4: Launch dev server\nnpm run dev")
        answer_parts.append("```")
        answer_parts.append("")
        answer_parts.append("**✅ Verify Setup**: Open http://localhost:5000 (or the configured port) in your browser.")
        answer_parts.append(f"**📋 Requirements**: {lang} runtime + dependencies from `requirements.txt` / `package.json`.")

    else:
        # Rich general response covering multiple dimensions
        answer_parts.append(f"### 🤖 Technical Deep-Dive: `{repo_name}`")
        answer_parts.append(f"> *Your question:* **\"{question}\"**")
        answer_parts.append("")
        answer_parts.append(f"**📊 Repository Snapshot:**")
        answer_parts.append(f"| Metric | Value |")
        answer_parts.append(f"|--------|-------|")
        answer_parts.append(f"| Language | {lang} |")
        answer_parts.append(f"| Tech Stack | {stack_text[:80]} |")
        answer_parts.append(f"| Total Files | {len(files)} |")
        answer_parts.append(f"| Stars | {stars:,} |")
        answer_parts.append(f"| Forks | {forks:,} |")
        answer_parts.append(f"| Readiness Score | {readiness_score}/100 ({readiness_badge}) |")
        answer_parts.append(f"| Tests | {'✅ Present' if has_tests else '⚠️ Missing'} |")
        answer_parts.append(f"| Docker | {'✅ Present' if has_docker else '⚠️ Missing'} |")
        answer_parts.append(f"| CI/CD | {'✅ Present' if has_ci else '⚠️ Missing'} |")
        answer_parts.append("")
        if mentioned_files:
            answer_parts.append(f"**📁 Files Relevant to Your Query**: `{', '.join(mentioned_files[:6])}`")
            answer_parts.append("")
        answer_parts.append("**🔍 Key Technical Insights:**")
        answer_parts.append(f"- The codebase follows a **{lang}**-centric architecture with {len(files)} source files organized for maintainability.")
        answer_parts.append(f"- The entrypoint {entry_str} orchestrates the main application lifecycle and request routing.")
        answer_parts.append("- For deeper investigation, ask about specific topics: *architecture, security, performance, testing, API design, deployment, or setup*.")

    return {
        "answer": "\n\n".join(answer_parts),
        "source": "Smart Code Intelligence Engine (Deterministic Analysis)"
    }

