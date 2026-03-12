import subprocess
import json


def compile_solidity(file):

    result = subprocess.run(
        ["solc", "--combined-json", "ast", file],
        capture_output=True,
        text=True,
        check=True
    )

    ast_json = json.loads(result.stdout)

    return ast_json["sources"][file]["AST"]
