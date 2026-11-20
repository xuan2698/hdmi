import ast
import json
import random
import resource
import sys


def main():
    resource.setrlimit(resource.RLIMIT_CPU, (3, 3))
    resource.setrlimit(resource.RLIMIT_AS, (160_000_000, 160_000_000))
    request = json.load(sys.stdin)
    tree = ast.parse(request["source"])
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom, ast.Global, ast.Nonlocal, ast.ClassDef)):
            raise ValueError(f"Forbidden Python construct: {type(node).__name__}")
        if isinstance(node, ast.Name) and node.id.startswith("_"):
            raise ValueError("Private names are unavailable")
        if isinstance(node, ast.Attribute) and node.attr.startswith("_"):
            raise ValueError("Private attributes are unavailable")
    names = ("abs", "all", "any", "bool", "dict", "enumerate", "int", "len",
             "list", "max", "min", "range", "reversed", "set", "sorted", "sum", "tuple", "zip")
    import builtins
    scope = {"__builtins__": {name: getattr(builtins, name) for name in names}}
    exec(compile(tree, "<model source>", "exec"), scope)
    if request["kind"] == "checker":
        result = scope["reference"](request["vectors"])
    else:
        result = scope["stimulus"](random.Random(request["seed"]), request["cycles"])
    json.dump(result, sys.stdout, allow_nan=False)


if __name__ == "__main__":
    main()
