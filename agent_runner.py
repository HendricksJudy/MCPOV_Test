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
