import sys
from flow import create_code_generator_flow

def main():
    """Runs the PocketFlow Code Generator application."""
    print("Starting PocketFlow Code Generator...")
    
    question = "what is the content in the file of test.txt?"

    shared = {
        "question": question,
        # "test_cases": [],  # Will be populated with [{name, input, expected}, ...]
        # "function_code": "",
        # "test_results": [],
        # "iteration_count": 0,
        # "max_iterations": 5
    }

    # Create and run the flow
    flow = create_code_generator_flow()
    flow.run(shared)
    
    # print("\n=== Final Results ===")
    # print(f"Problem: {shared['problem'][:50]}...")
    # print(f"Iterations: {shared['iteration_count']}")
    # print(f"Function:\n{shared['function_code']}")
    # print(f"Test Results: {len([r for r in shared['test_results'] if r['passed']])}/{len(shared['test_results'])} passed")

if __name__ == "__main__":
    main() 