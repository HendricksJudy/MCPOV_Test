import asyncio
import os
from mcp_agent.agents.agent import Agent
from mcp_agent.workflows.llm.augmented_llm_openai import OpenAIAugmentedLLM
from mcp_agent.config import Settings, OpenAISettings
from mcp_agent.core.context import initialize_context

DOC_SERVER = "http://localhost:8000"


async def main():
    cfg = Settings(
        openai=OpenAISettings(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=(
                os.getenv("OPENAI_BASE_URL")
                or os.getenv("OPENAI_API_BASE")
            ),
        )
    )
    context = await initialize_context(cfg)
    bot = Agent(
        name="omics_doc_bot",
        instruction=(
            "Return the OmicVerse docstring for the requested function; "
            "respond with 'Not documented' if missing."
        ),
        server_names=[DOC_SERVER],
        context=context,
    )

    async with bot:
        llm = await bot.attach_llm(OpenAIAugmentedLLM)
        resp = await llm.generate_str("Explain ov.utils.cluster")
        print(resp)

if __name__ == "__main__":
    asyncio.run(main())
