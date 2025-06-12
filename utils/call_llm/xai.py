from openai import OpenAI, AsyncOpenAI
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()

# Learn more about calling the LLM: https://the-pocket.github.io/PocketFlow/utility_function/llm.html
def _call_llm_sync(prompt):
    """Synchronous wrapper for XAI API call."""
    client = OpenAI(
        api_key=os.environ.get("XAI_API_KEY"),
        base_url="https://api.x.ai/v1"
    )
    r = client.chat.completions.create(
        model="grok-3",
        messages=[{"role": "user", "content": prompt}]
    )
    return r.choices[0].message.content

async def _call_llm_async(prompt):
    """Asynchronous wrapper for XAI API call."""
    client = AsyncOpenAI(
        api_key=os.environ.get("XAI_API_KEY"),
        base_url="https://api.x.ai/v1"
    )
    r = await client.chat.completions.create(
        model="grok-3",
        messages=[{"role": "user", "content": prompt}]
    )
    return r.choices[0].message.content

def call_llm(prompt, is_async=False):
    """Main function to call XAI API, supporting both sync and async modes."""
    if is_async:
        return _call_llm_async(prompt)
    return _call_llm_sync(prompt)

if __name__ == "__main__":
    async def run_test():
        print("## Testing XAI LLM calls")
        prompt = "Testing. Just say hi and hello world and nothing else."
        print(f"## Prompt: {prompt}")
        
        # Test sync call
        print("\n## Testing sync call:")
        response = call_llm(prompt)
        print(f"## Response: {response}")
        
        # Test async call
        print("\n## Testing async call:")
        response = await call_llm(prompt, is_async=True)
        print(f"## Response: {response}")

    asyncio.run(run_test())
