from typing import Dict, Any
from app.engine.graph import Graph, Node
from app.engine.registry import ToolRegistry

# -----------------------------
# TOOL FUNCTIONS (AGENT LOGIC)
# -----------------------------

def extract_functions(state: Dict[str, Any], **kwargs):
    code = state.get('code', '')

    funcs = []
    lines = code.splitlines()
    cur = []
    collecting = False

    for line in lines:
        if line.strip().startswith('def '):
            if cur:
                funcs.append("\n".join(cur))
                cur = []
            collecting = True
            cur.append(line)
        else:
            if collecting:
                cur.append(line)

    if cur:
        funcs.append("\n".join(cur))

    state['functions'] = funcs
    state['extracted'] = len(funcs)
    return {"extracted": len(funcs)}


def check_complexity(state: Dict[str, Any], **kwargs):
    funcs = state.get('functions', [])

    complexities = []
    for f in funcs:
        c = 0
        for line in f.splitlines():
            if line.strip().startswith(('if ', 'for ', 'while ')):
                c += 1
        c += max(0, len(f.splitlines()) - 5)
        complexities.append(c)

    state['complexities'] = complexities

    avg = sum(complexities) / (len(complexities) or 1)
    quality = max(0, 100 - int(avg * 10))
    state['quality_score'] = quality

    return {"complexities": complexities, "quality_score": quality}


def detect_issues(state: Dict[str, Any], **kwargs):
    funcs = state.get('functions', [])
    issues = []

    for f in funcs:
        if "TODO" in f or "FIXME" in f:
            issues.append("todo_found")
        if "print(" in f:
            issues.append("debug_prints")
        if "eval(" in f:
            issues.append("uses_eval")

    state['issues'] = issues
    state['quality_score'] = max(0, state['quality_score'] - len(issues) * 5)

    return {"issues": issues, "quality_score": state['quality_score']}


def suggest_improvements(state: Dict[str, Any], **kwargs):
    suggestions = []

    for i, c in enumerate(state.get("complexities", [])):
        if c > 10:
            suggestions.append(f"Function {i} is too complex → consider refactoring")

    if "debug_prints" in state.get("issues", []):
        suggestions.append("Remove print() and use proper logging.")

    if "uses_eval" in state.get("issues", []):
        suggestions.append("Avoid using eval() — it is dangerous.")

    state["suggestions"] = suggestions
    state["quality_score"] = min(100, state["quality_score"] + len(suggestions) * 2)

    return {"suggestions": suggestions, "quality_score": state["quality_score"]}


# REGISTER TOOLS
ToolRegistry.register("extract_functions", extract_functions)
ToolRegistry.register("check_complexity", check_complexity)
ToolRegistry.register("detect_issues", detect_issues)
ToolRegistry.register("suggest_improvements", suggest_improvements)


# -----------------------------------
# CREATE SAMPLE GRAPH (WORKFLOW)
# -----------------------------------

def build_sample_graph() -> Graph:
    nodes = {
        "extract": Node(name="extract", func_name="extract_functions"),
        "complexity": Node(name="complexity", func_name="check_complexity"),
        "issues": Node(name="issues", func_name="detect_issues"),
        "suggest": Node(name="suggest", func_name="suggest_improvements"),
    }

    edges = {
        "extract": "complexity",
        "complexity": "issues",
        "issues": "suggest",
        "suggest": None,
    }

    loops = {
        "suggest": {
            "until": "quality_score",
            "threshold": 85,
            "goto": "complexity"
        }
    }

    return Graph(nodes=nodes, edges=edges, start="extract", loops=loops)
