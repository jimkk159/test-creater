import os
from google import genai
from dotenv import load_dotenv
import asyncio

load_dotenv()

def _call_llm_sync(prompt):
    """Synchronous wrapper for Gemini API call."""
    client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))
    response = client.models.generate_content(
        model="gemini-2.5-pro-preview-06-05", contents=prompt
    )
    return response.text

async def _call_llm_async(prompt):
    """Asynchronous wrapper for Gemini API call."""
    # Since Gemini's client doesn't have native async support,
    # we'll run the sync version in a thread pool
    return await asyncio.to_thread(_call_llm_sync, prompt)

def call_llm(prompt, is_async=False):
    """Main function to call Gemini API, supporting both sync and async modes."""
    if is_async:
        return _call_llm_async(prompt)
    return _call_llm_sync(prompt)

if __name__ == "__main__":
    async def run_test():
        print("## Testing Gemini LLM calls")
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
