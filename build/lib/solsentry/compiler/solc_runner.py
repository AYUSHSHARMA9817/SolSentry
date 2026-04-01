import subprocess
import json
import os

def find_project_root(file_path):
    cur = os.path.abspath(os.path.dirname(file_path))

    while cur != "/":
        if os.path.exists(os.path.join(cur, "lib")) or \
           os.path.exists(os.path.join(cur, "node_modules")):
            return cur
        cur = os.path.dirname(cur)

    return os.getcwd()

def load_remappings(root):
    path = os.path.join(root, "remappings.txt")

    if not os.path.exists(path):
        return []

    remappings = []

    with open(path) as f:
        for line in f:
            line = line.strip()

            # skip empty / invalid lines
            if not line or "=" not in line:
                continue

            remappings.append(line)

    return remappings
    
def compile_solidity(file):
    project_root = find_project_root(file)
    rel_path = os.path.relpath(file,project_root)
    remappings = load_remappings(project_root)

    cmd = [
        "solc",
        "--combined-json", "ast",
        "--base-path", project_root,
        "--include-path", os.path.join(project_root, "lib"),
    ]

    for r in remappings:
        cmd.extend([r])

    cmd.append(rel_path)
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=project_root
    )

    if result.returncode != 0:
        print("SOLC ERROR:\n", result.stderr)
        raise Exception("Solc failed")

    ast_json = json.loads(result.stdout)

    return ast_json["sources"][rel_path]["AST"]
