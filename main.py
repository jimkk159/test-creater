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

#     test_code = """
#     describe('add function', () => {
#         const add = async (a, b) => a + b;
        
#         test('Basic case - positive integers', async () => {
#             expect(await add(1, 1)).toBe(2);
#         });

#         test('Basic case - positive integers', async () => {
#             expect(await add(1, 2)).toBe(2);
#         });
#     });
    
#     describe('subtract function', () => {
#         const subtract = async (a, b) => a - b;
        
#         test('Basic case - positive integers', async () => {
#             expect(await add(1, 1)).toBe(1);
#         });

#         test('Basic case - positive integers', async () => {
#             expect(await add(1, 2)).toBe(2);
#         });
#     });
    
# """
    
    shared = {
        "question": question,
        "file": {},
        "analyze": {},
        "test_code": "",
        "test_cases": {},
        "functions": {'add': 'const add = (a, b) => a + b\n', 'multiple': 'const multiple = (a, b) => a * b'}
    }
    shared = {
  "question": "what is the content in the file myMath.js!",
  "action": "done",
  "parameters": {},
  "thinking": "The question asks for the content of the file myMath.js. The previous action has already retrieved the content of that file successfully. Therefore, there is no further action needed to extract or analyze information from it.",
  "tool_result": "const add = (a, b)=> a+b \nconst multiple = (a, b)=> a * b \n\nmodule.exports = { add, multiple }",
  "result": "✅ FILE CONTENT:\nconst add = (a, b)=> a+b \nconst multiple = (a, b)=> a * b \n\nmodule.exports = { add, multiple }",
  "analyze": {
    "file_content": "const add = (a, b)=> a+b \nconst multiple = (a, b)=> a * b \n\nmodule.exports = { add, multiple }"
  },
  "test_code": {},
  "test_cases": {},
  "functions": {
    "add": "const add = (a, b) => a + b \n",
  }
}

    # Create and run the flow
    flow = auto_code_test_generate_flow()
    await flow.run_async(shared)

    # print("\n=== Final Results ===")
    # print(f"Problem: {shared['problem'][:50]}...")
    # print(f"Iterations: {shared['iteration_count']}")
    # print(f"Function:\n{shared['function_code']}")
    # print(f"Test Results: {len([r for r in shared['test_results'] if r['passed']])}/{len(shared['test_results'])} passed")

if __name__ == "__main__":
    asyncio.run(main()) 