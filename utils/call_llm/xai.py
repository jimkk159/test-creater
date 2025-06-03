from openai import OpenAI

import os
from dotenv import load_dotenv

load_dotenv()

# Learn more about calling the LLM: https://the-pocket.github.io/PocketFlow/utility_function/llm.html
def call_llm(prompt):    
    client = OpenAI(api_key=os.environ.get("XAI_API_KEY"),     base_url="https://api.x.ai/v1",)
    r = client.chat.completions.create(
        model="grok-3",
        messages=[{"role": "user", "content": prompt}]
    )
    return r.choices[0].message.content
    
if __name__ == "__main__":
    prompt = "Testing. Just say hi and hello world and nothing else."
    print(call_llm(prompt))
