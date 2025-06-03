import os
import asyncio
from anthropic import AsyncAnthropic
from dotenv import load_dotenv

load_dotenv()

# Async version of the simple wrapper, using Anthropic
async def call_llm(prompt):
    """Async wrapper for Anthropic API call."""
    client = AsyncAnthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    response = await client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=20000,
        # thinking={
        #     "type": "enabled",
        #     "budget_tokens": 16000
        # },
        messages=[
            {"role": "user", "content": prompt}
        ],
    )

    return response.content[0].text

if __name__ == "__main__":
    async def run_test():
        print("## Testing async call_llm with Anthropic")
        prompt = "Testing. Just say hi and hello world and nothing else."
        print(f"## Prompt: {prompt}")
        response = await call_llm(prompt)
        print(f"## Response: {response}")

    asyncio.run(run_test()) 