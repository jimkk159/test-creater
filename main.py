import sys
import asyncio
from flow import auto_code_test_generate_flow

BORDER_LEN = 96
border = f"{"=" * BORDER_LEN}"

async def main():
    """Runs the PocketFlow Code Generator application."""
    print(border)
    print("Starting PocketFlow Code Generator...")
    
    question = "what is the content in the file myMath.js!"
    
    shared = {
        "question": question,
    }

    # Create and run the flow
    flow = auto_code_test_generate_flow()
    await flow.run_async(shared)

    print("\n=== Final Results ===")
    print(f"Problem: {shared['problem'][:50]}...")
    print(f"Iterations: {shared['iteration_count']}")
    print(f"Function:\n{shared['function_code']}")
    print(f"Test Results: {len([r for r in shared['test_results'] if r['passed']])}/{len(shared['test_results'])} passed")

if __name__ == "__main__":
    asyncio.run(main()) 