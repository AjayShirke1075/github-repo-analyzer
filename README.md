# ⚡ AI GitHub Repository Intelligence & Developer Platform

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0+-000000?style=for-the-badge&logo=flask&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Gemini_1.5_Flash-8E75B2?style=for-the-badge&logo=google&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI_GPT--4o-412991?style=for-the-badge&logo=openai&logoColor=white)
![ReportLab](https://img.shields.io/badge/PDF_Generation-ReportLab-red?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)

**A Production-Ready AI Developer Platform for Deep Architectural Audits, Automated Code Reviews, and Technical Interview Preparation.**

</div>

---

## 🌟 Overview

The **AI GitHub Repository Intelligence Platform** is an enterprise-grade developer tool designed to analyze any public GitHub codebase and generate deep, actionable engineering audits. Built specifically to showcase mastery in applied AI, system design, and developer tooling during **AI Developer / Software Engineer technical interviews**.

The platform features a **Multi-Model AI Engine** that works seamlessly across **Google Gemini 1.5 Flash**, **OpenAI GPT-4o-mini**, or an offline **Deterministic Static Intelligence Engine**—guaranteeing 100% reliable interview demonstrations with zero API costs.

---

## 🚀 Key Features

### 1. 🤖 Multi-Provider AI Architecture Engine
- **Provider Agnostic**: Switch on-the-fly between **Google Gemini (Free tier/High speed)**, **OpenAI (GPT-4o-mini)**, and the **Built-in Smart Local Engine**.
- **Zero-Cost & Quota Resilience**: Automatically falls back to local AST & deterministic engineering heuristics if API keys are missing, invalid, or out of quota. It never crashes or shows a blank screen during a demo.
- **Audits**:
  - 🏗️ Architectural Design Patterns & Modularity (Layering, Factory Patterns, Separation of Concerns).
  - 🛡️ Security & Vulnerability Analysis (OWASP risks, credential hygiene, input sanitization).
  - ⚡ Scalability & Performance Bottlenecks (Blocking I/O, caching strategies, horizontal scaling).
  - 🧪 Automated Testing & CI/CD pipeline maturity.

### 2. 🔍 Automated Entrypoint Discovery & Code Review
- Automatically scans the file tree to locate the primary application entrypoint (`app.py`, `main.py`, `server.js`, `main.go`, etc.).
- Safely pulls and inspects live source code without cloning the whole repo.
- Generates line-level feedback on code smells, resource leaks, bare exceptions, and refactoring diffs.

### 3. 🎯 AI Technical Interview Preparation Mode
- Designed directly for candidates preparing for technical interviews!
- Generates **5 deep technical interview questions** specifically tailored to the analyzed repository.
- Provides model candidate answers, concepts the interviewer is evaluating, and architectural talking points.

### 4. 🎯 AI Project Intent vs. Reality Auditor
- Compares a developer's claimed project goals or README intent against actual codebase implementation.
- Computes an **Alignment Score (0-100%)** and isolates:
  - ✅ Confirmed Matches (features proven by code evidence).
  - ⚠️ Architectural Warnings (partially implemented layers).
  - ❌ Missing Core Modules (unimplemented claims).

### 5. 💼 AI Resume & Job Fit Matcher
- Evaluates candidate resumes or target job descriptions against the repository's technologies and structure.
- Calculates skill match percentages and provides a tailored candidate interview pitch highlighting the project's evidence.

### 6. 📄 Dynamic On-The-Fly PDF Report Generator
- Powered by ReportLab Flowables.
- Generates a customized, multi-page professional PDF report featuring repository metrics, readiness scorecards, full AI reviews, and interview Q&As.

### 7. 🧩 Visual System Diagrams & Workflows
- **Architecture Pipeline**: Illustrates data flow (Client → API Router → Service Handlers → Database → Output).
- **Module Dependency Graph**: Visualizes core code modules and configuration files.
- **File Hierarchy Tree**: High-level structural tree diagram.

### 8. 💬 Live Interactive AI Codebase Assistant
- In-browser chat box allowing interviewers to ask real-time questions about the repository (e.g., *"How is authentication implemented?"*, *"What caching is used?"*).

---

## 🛠️ Architecture & Tech Stack

| Layer | Technologies |
| :--- | :--- |
| **Backend Core** | Python 3.10+, Flask 3.1, Werkzeug |
| **AI / LLM Integration** | Google Gemini (`google-generativeai`), OpenAI (`openai`), Python-Dotenv |
| **GitHub Data Layer** | PyGithub (Optimized single-request Git Tree API & multi-tier token fallback) |
| **PDF Generation** | ReportLab 5.1 (Multi-page dynamic flowables, custom styling) |
| **Diagram Engine** | Graphviz (`Digraph`) with safe fallback handling |
| **Frontend UI** | HTML5, CSS3 Tokens, Vanilla JavaScript, Marked.js, Inter & Fira Code fonts |

---

## ⚡ Quick Start

### 1. Clone & Setup Virtual Environment
```bash
git clone https://github.com/your-username/github-repo-analyzer.git
cd github-repo-analyzer

# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure API Keys (Optional)
Create a `.env` file in the project root (or input keys directly in the web UI):
```env
# Optional: Free tier Google Gemini key (https://aistudio.google.com/)
GEMINI_API_KEY=your_gemini_key_here

# Optional: OpenAI key
OPENAI_API_KEY=your_openai_key_here

# Optional: GitHub token for 5,000 requests/hour (Anonymous gives 60/hr)
GITHUB_TOKEN=your_github_token_here
```
*(Note: If no API key is provided, the platform automatically runs on the built-in Smart Local Engine!)*

### 4. Run the Application
```bash
python app.py
```
Open your browser at:
```
http://127.0.0.1:5000
```

---

## 💡 How to Demo in an AI Developer Interview

1. **Highlight the Architecture**: Explain how you separated concerns into modular utilities (`ai_engine.py`, `github_analyzer.py`, `pdf_report_generator.py`).
2. **Discuss Multi-Tier Fallback Strategy**: Demonstrate how the system gracefully handles rate limits and API quota exhaustion using a deterministic fallback engine.
3. **Showcase Git Tree API Optimization**: Point out how switching from recursive `get_contents` to `get_git_tree` reduced network round-trips from 50+ HTTP calls to 1 single call.
4. **Demonstrate Interview Mode**: Analyze a popular open-source project (e.g. `pallets/flask` or your own projects) and show the AI Technical Interview Q&A tab.
5. **Export the PDF Report**: Click "Download AI Audit Report (PDF)" to show dynamic document compilation with ReportLab.

---

## 📄 License
MIT License. Open source and portfolio ready.
