import os
from graphviz import Digraph


def generate_structure_diagram(repo_name, files):
    """
    Creates a repository structure diagram (tree-like)
    Output: static/diagrams/structure.png
    Returns: relative path for HTML
    """
    output_dir = os.path.join("static", "diagrams")
    os.makedirs(output_dir, exist_ok=True)

    dot = Digraph(comment="Repo Structure", format="png")
    dot.attr(rankdir="LR")

    root = repo_name.replace("/", "_")
    dot.node(root, repo_name, shape="folder")

    for path in files:
        parts = path.split("/")
        current = root

        for i, part in enumerate(parts):
            node_id = f"{current}/{part}".replace("/", "_")

            if i == len(parts) - 1:
                dot.node(node_id, part, shape="note")
            else:
                dot.node(node_id, part, shape="folder")

            dot.edge(current, node_id)
            current = node_id

    output_path = os.path.join(output_dir, "structure")
    dot.render(output_path, cleanup=True)

    return "diagrams/structure.png"


def generate_dependency_flowchart(repo_name, files):
    """
    Creates a basic dependency flowchart (rule-based)
    Output: static/diagrams/dependencies.png
    Returns: relative path for HTML
    """
    output_dir = os.path.join("static", "diagrams")
    os.makedirs(output_dir, exist_ok=True)

    dot = Digraph(comment="Repo Dependencies", format="png")
    dot.attr(rankdir="LR")

    root = repo_name.replace("/", "_")
    dot.node(root, repo_name, shape="box")

    py_files = [f for f in files if f.endswith(".py")]

    if not py_files:
        dot.node("no_py", "No Python files found", shape="note")
        dot.edge(root, "no_py")
    else:
        for f in py_files:
            node_id = f.replace("/", "_")
            dot.node(node_id, f, shape="note")
            dot.edge(root, node_id)

    output_path = os.path.join(output_dir, "dependencies")
    dot.render(output_path, cleanup=True)

    return "diagrams/dependencies.png"


def generate_how_it_works_diagram(repo_name, tech_stack):
    """
    Creates a block diagram showing HOW the code works
    Output: static/diagrams/how_it_works.png
    Returns: relative path for HTML
    """
    output_dir = os.path.join("static", "diagrams")
    os.makedirs(output_dir, exist_ok=True)

    dot = Digraph(comment="How Code Works", format="png")
    dot.attr(rankdir="LR")

    # Blocks
    dot.node("A", "User enters GitHub URL", shape="box")
    dot.node("B", "GitHub Analyzer\n(fetch repo info + files)", shape="box")
    dot.node("C", "Tech Stack Detector\n(detect technologies)", shape="box")
    dot.node("D", "Project Intent Checker\n(intent vs repo reality)", shape="box")
    dot.node("E", "Repo Readiness Checker\n(score + badge)", shape="box")
    dot.node("F", "Flowchart Generator\n(structure + dependencies)", shape="box")
    dot.node("G", "Final Dashboard Output\n(render HTML report)", shape="box")

    # Flow
    dot.edge("A", "B")
    dot.edge("B", "C")
    dot.edge("C", "D")
    dot.edge("D", "E")
    dot.edge("E", "F")
    dot.edge("F", "G")

    # Show tech stack in note box (optional)
    if tech_stack:
        stack_text = "Tech Stack:\\n" + "\\n".join(tech_stack[:10])
        dot.node("TS", stack_text, shape="note")
        dot.edge("C", "TS", style="dashed")

    output_path = os.path.join(output_dir, "how_it_works")
    dot.render(output_path, cleanup=True)

    return "diagrams/how_it_works.png"
