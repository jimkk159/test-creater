import sys
import asyncio
from flow import auto_code_test_generate_flow

BORDER_LEN = 96
border = f"{"=" * BORDER_LEN}"

async def main():
    """Runs the PocketFlow Code Generator application."""
    print(border)
    print("Starting PocketFlow Code Generator...")
    
    question = "what is the content in the file test/myMath.js!"
    
    shared = {
        "question": question,
    }

    # Create and run the flow
    flow = auto_code_test_generate_flow()
    await flow.run_async(shared)

    # print("\n=== Final Results ===")
    # print(f"Problem: {shared['question'][:50]}...")
    # print(f"Final Result:\n{shared['final_result']}")

if __name__ == "__main__":
    asyncio.run(main()) 