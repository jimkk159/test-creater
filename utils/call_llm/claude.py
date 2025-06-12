from anthropic import Anthropic, AsyncAnthropic
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()

def _call_llm_sync(prompt):
    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000
    )
    return response.content[0].text

async def _call_llm_async(prompt):
    client = AsyncAnthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    response = await client.messages.create(
        model="claude-sonnet-4-20250514",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000
    )
    return response.content[0].text

def call_llm(prompt, is_async=False):
    if is_async:
        return _call_llm_async(prompt)
    return _call_llm_sync(prompt)

if __name__ == "__main__":
    prompt = "Testing. Just say hi and hello world and nothing else."
    print(call_llm(prompt))  # Sync call
    # For async test:
    # asyncio.run(call_llm(prompt, is_async=True)) 