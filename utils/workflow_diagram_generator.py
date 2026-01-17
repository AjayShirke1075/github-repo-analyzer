import os
import re
from graphviz import Digraph


def find_entry_file(files):
    """
    Finds most likely entry file in repo.
    Priority: app.py > main.py > run.py > server.py > index.py
    """
    priority = ["app.py", "main.py", "run.py", "server.py", "index.py"]

    for p in priority:
        if p in files:
            return p

    # fallback: first python file
    for f in files:
        if f.endswith(".py") and "/" not in f:
            return f

    return None


def parse_imports_and_calls(file_content):
    """
    Extract simple imports and function calls (rule-based, no AI).
    """
    imports = set()
    calls = set()

    # imports
    for line in file_content.splitlines():
        line = line.strip()

        # import xyz
        m1 = re.match(r"import\s+([a-zA-Z0-9_\.]+)", line)
        if m1:
            imports.add(m1.group(1))

        # from xyz import abc
        m2 = re.match(r"from\s+([a-zA-Z0-9_\.]+)\s+import\s+(.+)", line)
        if m2:
            imports.add(m2.group(1))

    # function calls pattern: something(...)
    call_matches = re.findall(r"([a-zA-Z_][a-zA-Z0-9_]*)\(", file_content)
    for c in call_matches:
        # filter common python keywords/known functions
        if c not in ["print", "len", "range", "open", "int", "str", "float", "list", "dict", "set", "tuple"]:
            calls.add(c)

    return sorted(imports), sorted(calls)


def generate_workflow_diagram(repo, repo_name, files):
    """
    ✅ Generates a 'How Code Works' block diagram for ANY GitHub repo.
    Reads entry file + detects imports + function calls.
    Output saved in: static/diagrams/workflow.png
    Returns: relative path for HTML => "diagrams/workflow.png"
    """

    output_dir = os.path.join("static", "diagrams")
    os.makedirs(output_dir, exist_ok=True)

    entry = find_entry_file(files)

    dot = Digraph(comment="Project Workflow", format="png")
    dot.attr(rankdir="TB")

    root = repo_name.replace("/", "_")
    dot.node(root, repo_name, shape="box", style="filled", color="lightblue")

    if not entry:
        dot.node("no_entry", "No entry file found (app.py/main.py)", shape="note")
        dot.edge(root, "no_entry")
    else:
        dot.node("entry", f"Entry File: {entry}", shape="folder")
        dot.edge(root, "entry")

        try:
            content_obj = repo.get_contents(entry)
            content = content_obj.decoded_content.decode("utf-8", errors="ignore")
        except Exception:
            content = ""

        imports, calls = parse_imports_and_calls(content)

        # imports block
        if imports:
            dot.node("imports", "Imports / Modules", shape="box")
            dot.edge("entry", "imports")

            for i, imp in enumerate(imports[:12]):  # limit to 12 for clean diagram
                node_id = f"imp_{i}"
                dot.node(node_id, imp, shape="note")
                dot.edge("imports", node_id)

        # calls block
        if calls:
            dot.node("calls", "Detected Function Calls", shape="box")
            dot.edge("entry", "calls")

            for i, call in enumerate(calls[:12]):  # limit to 12
                node_id = f"call_{i}"
                dot.node(node_id, call + "()", shape="note")
                dot.edge("calls", node_id)

        # output block
        dot.node("output", "Generated Output\n• Repo Overview\n• Tech Stack\n• Readiness\n• Diagrams", shape="box")
        dot.edge("entry", "output")

    output_path = os.path.join(output_dir, "workflow")
    dot.render(output_path, cleanup=True)

    return "diagrams/workflow.png"
