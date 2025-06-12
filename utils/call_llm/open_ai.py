from openai import OpenAI, AsyncOpenAI

import os
from dotenv import load_dotenv
import asyncio

load_dotenv()

# Learn more about calling the LLM: https://the-pocket.github.io/PocketFlow/utility_function/llm.html
def _call_llm_sync(prompt):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    r = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return r.choices[0].message.content

async def _call_llm_async(prompt):
    client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    r = await client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return r.choices[0].message.content

def call_llm(prompt, is_async=False):
    if is_async:
        return _call_llm_async(prompt)
    return _call_llm_sync(prompt)

if __name__ == "__main__":
    prompt = "Testing. Just say hi and hello world and nothing else."
    print(call_llm(prompt))  # Sync call
    # For async test:
    # asyncio.run(call_llm(prompt, is_async=True))
