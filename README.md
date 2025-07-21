# MCPOV_Test

This repository includes `ov_function_counts.csv` with the canonical OmicVerse function names. The steps below show how to expose documentation for these functions via a minimal MCP-compliant server without using embeddings.

## 1. Install prerequisites

```bash
pip install fastapi uvicorn mcp-agent
```

## 2. Clone the OmicVerse repository and extract docs

```bash
git clone https://github.com/Starlitnightly/omicverse.git
python build_function_docs.py omicverse
```

This creates `function_docs.json` containing the docstring for every function found in `ov_function_counts.csv`.

## 3. Start the doc server

```bash
uvicorn doc_server:app --host 0.0.0.0 --port 8000
```

The FastAPI server exposes an OpenAPI specification compatible with Model Context Protocol. The `doc` tool returns the stored docstring for a given function name.

## 4. Query via an agent

`agent_runner.py` demonstrates how a lastmile `mcp-agent` can retrieve a docstring:

```python
import asyncio
from mcp_agent.agents.agent import Agent
from mcp_agent.workflows.llm.augmented_llm_openai import OpenAIAugmentedLLM

DOC_SERVER = "http://localhost:8000"

async def main():
    bot = Agent(
        name="omics_doc_bot",
        instruction=(
            "Return the OmicVerse docstring for the requested function; respond with 'Not documented' if missing."),
        server_names=[DOC_SERVER]
    )

    async with bot:
        llm = await bot.attach_llm(OpenAIAugmentedLLM)
        resp = await llm.generate_str("Explain ov.utils.cluster")
        print(resp)

if __name__ == "__main__":
    asyncio.run(main())
```

Run the agent with:

```bash
OPENAI_API_KEY=... python agent_runner.py
```

This workflow serves exact documentation for each function using only the names listed in `ov_function_counts.csv`.
