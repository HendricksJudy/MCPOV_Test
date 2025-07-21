import ast
import csv
import json
import sys
import textwrap
from pathlib import Path

repo_root = Path(sys.argv[1] if len(sys.argv) > 1 else "omicverse")
csv_path = Path("ov_function_counts.csv")
output_path = Path("function_docs.json")

docs = {}
with csv_path.open() as f:
    reader = csv.DictReader(line for line in f if line.strip())
    for row in reader:
        func = row["Function"]
        parts = func.split(".")
        if len(parts) < 3 or parts[0] != "ov":
            continue
        module = parts[1]
        name = parts[2]
        search_dir = repo_root / module
        doc = None
        if search_dir.exists():
            for py in search_dir.rglob("*.py"):
                tree = ast.parse(py.read_text(encoding="utf-8"))
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef) and node.name == name:
                        doc = ast.get_docstring(node) or ""
                        doc = textwrap.dedent(doc).strip()
                        break
                if doc is not None:
                    break
        docs[func] = doc or ""

with output_path.open("w", encoding="utf-8") as f:
    json.dump(docs, f, indent=2, ensure_ascii=False)
print(f"Saved {len(docs)} docs to {output_path}")
