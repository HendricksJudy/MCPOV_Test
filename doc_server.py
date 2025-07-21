from fastapi import FastAPI, HTTPException
import json
import os

DATA_FILE = os.getenv("DOCS_FILE", "function_docs.json")

with open(DATA_FILE, encoding="utf-8") as f:
    DOCS = json.load(f)

app = FastAPI(title="OmicVerse Function Docs", version="0.1.0")

@app.get("/doc")
async def get_doc(function: str):
    """Return the stored docstring for a function name."""
    doc = DOCS.get(function)
    if not doc:
        raise HTTPException(status_code=404, detail="Function not found")
    return {"function": function, "doc": doc}
