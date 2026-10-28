"""
Diagram and Flowchart Generator for GitHub Repositories.
Generates repository structure, dependency graphs, and architecture workflow diagrams.
Includes safe execution guards against Graphviz missing-executable errors.
"""

import os
from typing import List, Optional
try:
    from graphviz import Digraph
    GRAPHVIZ_AVAILABLE = True
except ImportError:
    GRAPHVIZ_AVAILABLE = False


def _safe_render(dot, output_base_path: str) -> Optional[str]:
    """Renders Graphviz dot safely, returning png path or None on error."""
    try:
        dot.render(output_base_path, cleanup=True)
        return output_base_path + ".png"
    except Exception as e:
        print(f"[Diagram Notice] Graphviz render skipped ({e})")
        return None


def generate_structure_diagram(repo_name: str, files: List[str]) -> Optional[str]:
    """
    Creates a hierarchical repository structure diagram.
    Limits to top 30 key files/directories for diagram clarity.
    """
    if not GRAPHVIZ_AVAILABLE or not files:
        return None

    output_dir = os.path.join("static", "diagrams")
    os.makedirs(output_dir, exist_ok=True)

    dot = Digraph(comment="Repo Structure", format="png")
    dot.attr(rankdir="LR", bgcolor="transparent")
    dot.attr("node", fontname="Helvetica", fontsize="10", shape="folder", style="filled", fillcolor="#1e293b", fontcolor="#f8fafc", color="#3b82f6")
    dot.attr("edge", color="#64748b", arrowhead="vee")

    root = repo_name.replace("/", "_").replace("-", "_")
    dot.node(root, repo_name, shape="box3d", fillcolor="#1e3a8a", fontcolor="#ffffff")

    # Filter out deep node_modules, .git, venv
    clean_files = [f for f in files if not any(x in f for x in [".git/", "node_modules/", "venv/", "__pycache__"])]
    selected_files = clean_files[:25]

    created_nodes = {root}

    for path in selected_files:
        parts = path.split("/")
        current = root

        for i, part in enumerate(parts):
            node_id = f"{current}_{part}".replace("/", "_").replace("-", "_").replace(".", "_")

            if node_id not in created_nodes:
                created_nodes.add(node_id)
                if i == len(parts) - 1:
                    dot.node(node_id, part, shape="note", fillcolor="#0f172a", fontcolor="#93c5fd", color="#60a5fa")
                else:
                    dot.node(node_id, part, shape="folder", fillcolor="#1e293b", fontcolor="#e2e8f0", color="#3b82f6")

                dot.edge(current, node_id)
            current = node_id

    output_path = os.path.join(output_dir, "structure")
    result = _safe_render(dot, output_path)
    return "diagrams/structure.png" if result else None


def generate_dependency_flowchart(repo_name: str, files: List[str]) -> Optional[str]:
    """
    Creates a module dependency and component relationship graph.
    """
    if not GRAPHVIZ_AVAILABLE:
        return None

    output_dir = os.path.join("static", "diagrams")
    os.makedirs(output_dir, exist_ok=True)

    dot = Digraph(comment="Repo Dependencies", format="png")
    dot.attr(rankdir="LR", bgcolor="transparent")
    dot.attr("node", fontname="Helvetica", fontsize="10", style="filled", fillcolor="#1e293b", fontcolor="#f8fafc", color="#8b5cf6")
    dot.attr("edge", color="#94a3b8", arrowhead="vee")

    root = repo_name.replace("/", "_").replace("-", "_")
    dot.node(root, f"📦 {repo_name}", shape="component", fillcolor="#2e1065", fontcolor="#ffffff")

    code_files = [f for f in files if any(f.endswith(ext) for ext in [".py", ".js", ".ts", ".go", ".rs", ".java"])]
    
    # Categorize files
    core_modules = [f for f in code_files if "/" not in f or f.count("/") == 1][:12]
    config_files = [f for f in files if any(c in f.lower() for c in ["req", "package.json", "docker", "config", ".env"])][:4]

    for f in core_modules:
        node_id = "mod_" + f.replace("/", "_").replace(".", "_").replace("-", "_")
        dot.node(node_id, f, shape="box", fillcolor="#0f172a", fontcolor="#c4b5fd", color="#a855f7")
        dot.edge(root, node_id)

    for cfg in config_files:
        node_id = "cfg_" + cfg.replace("/", "_").replace(".", "_").replace("-", "_")
        dot.node(node_id, f"⚙️ {cfg}", shape="cylinder", fillcolor="#1e293b", fontcolor="#fde047", color="#eab308")
        dot.edge(root, node_id, style="dashed")

    output_path = os.path.join(output_dir, "dependencies")
    result = _safe_render(dot, output_path)
    return "diagrams/dependencies.png" if result else None


def generate_how_it_works_diagram(repo_name: str, tech_stack: List[str]) -> Optional[str]:
    """
    Dynamically generates an architectural pipeline diagram reflecting
    how the target repository operates based on its detected architecture.
    """
    if not GRAPHVIZ_AVAILABLE:
        return None

    output_dir = os.path.join("static", "diagrams")
    os.makedirs(output_dir, exist_ok=True)

    dot = Digraph(comment="How Code Works", format="png")
    dot.attr(rankdir="LR", bgcolor="transparent")
    dot.attr("node", fontname="Helvetica", fontsize="10", shape="box", style="filled,rounded", fillcolor="#1e293b", fontcolor="#f8fafc", color="#06b6d4")
    dot.attr("edge", color="#38bdf8", arrowhead="vee", penwidth="1.2")

    stack_str = ", ".join(tech_stack[:3]) if tech_stack else "System"

    if any(t in tech_stack for t in ["Flask", "Django", "FastAPI", "Node.js", "Express"]):
        # Web / API Architecture
        dot.node("client", "🌐 Client / User\n(HTTP Requests)", fillcolor="#0e7490", fontcolor="#ffffff")
        dot.node("routing", f"🚦 API Gateway / Router\n({stack_str})", fillcolor="#1e293b")
        dot.node("controllers", "⚙️ Business Logic\n(Services & Handlers)", fillcolor="#1e293b")
        dot.node("data", "💾 Persistence / Storage\n(Database / Models)", fillcolor="#1e293b")
        dot.node("response", "📊 Response Pipeline\n(JSON / Rendered UI)", fillcolor="#0f766e", fontcolor="#ffffff")

        dot.edge("client", "routing", label="request")
        dot.edge("routing", "controllers", label="dispatch")
        dot.edge("controllers", "data", label="CRUD / query")
        dot.edge("data", "controllers", label="dataset")
        dot.edge("controllers", "response", label="serialize")
        dot.edge("response", "client", label="200 OK / view", style="dashed")
    else:
        # General Software Pipeline
        dot.node("input", "📥 Input Ingestion\n(CLI / Config / Data)", fillcolor="#0e7490", fontcolor="#ffffff")
        dot.node("parser", f"⚙️ Core Engine\n({stack_str})", fillcolor="#1e293b")
        dot.node("processing", "🔄 Transformation &\nExecution Pipeline", fillcolor="#1e293b")
        dot.node("output", "📤 Output & Telemetry\n(Artifacts / Reports)", fillcolor="#0f766e", fontcolor="#ffffff")

        dot.edge("input", "parser")
        dot.edge("parser", "processing")
        dot.edge("processing", "output")

    output_path = os.path.join(output_dir, "how_it_works")
    result = _safe_render(dot, output_path)
    return "diagrams/how_it_works.png" if result else None
