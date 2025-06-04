import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

# Async version of the simple wrapper, using Anthropic
def call_llm(prompt):
    """Async wrapper for Anthropic API call."""
    client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))
    response = client.models.generate_content(
        model="gemini-2.5-pro-preview-05-06", contents=prompt
    )

    return response.text

if __name__ == "__main__":
    def run_test():
        print("## Testing async call_llm with Anthropic")
        prompt = "Testing. Just say hi and hello world and nothing else."
        print(f"## Prompt: {prompt}")
        response = call_llm(prompt)
        print(f"## Response: {response}")

    run_test()
