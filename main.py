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
    }
#     shared = {
#         'question': 'what is the content in the file myMath.js!',
#         'test_code': '''describe('add function', () => {
#     const add = async (a, b) => a + b;

#     test('Basic case with positive numbers', async () => {
#         expect(await add(2, 3)).toBe(5);
#     });

#     test('Basic case with negative numbers', async () => {
#         expect(await add(-1, -2)).toBe(-3);
#     });

#     test('Edge case - adding zero', async () => {
#         expect(await add(5, 0)).toBe(5);
#     });

#     test('Edge case - adding two zeros', async () => {
#         expect(await add(0, 0)).toBe(0);
#     });

#     test('Type case - adding a number and a string', async () => {
#         await expect(add('3', 2)).rejects.toThrow("3 is not a number");
#     });

#     test('Type case - adding an object', async () => {
#         await expect(add({}, 5)).rejects.toThrow("[object Object] is not a number");
#     });
# });''',
#         'functions': [
#             {'add': 'const add = async (a, b) => a + b;'}
#         ],
#         'test_cases': {
#             'add': [
#                 {
#                     'name': 'Basic case with positive numbers',
#                     'explain': 'Testing the addition of two positive integers.',
#                     'input': {'a': 2, 'b': 3},
#                     'expected': 5
#                 },
#                 {
#                     'name': 'Basic case with negative numbers',
#                     'explain': 'Testing the addition of two negative integers.',
#                     'input': {'a': -1, 'b': -2},
#                     'expected': -3
#                 },
#                 {
#                     'name': 'Edge case - adding zero',
#                     'explain': 'Testing the addition of a number to zero.',
#                     'input': {'a': 5, 'b': 0},
#                     'expected': 5
#                 },
#                 {
#                     'name': 'Edge case - adding two zeros',
#                     'explain': 'Testing the addition of zero to zero.',
#                     'input': {'a': 0, 'b': 0},
#                     'expected': 0
#                 },
#                 {
#                     'name': 'Type case - adding a number and a string',
#                     'explain': 'Testing if the function handles a string input as first parameter.',
#                     'input': {'a': '3', 'b': 2},
#                     'expected': '3 is not a number'
#                 },
#                 {
#                     'name': 'Type case - adding an object',
#                     'explain': 'Testing if the function handles an object input.',
#                     'input': {'a': {}, 'b': 5},
#                     'expected': '{} is not a number'
#                 }
#             ]
#         },
#         'max_iterations': 5,
#         'iteration_count': 1,
#         'passed': 4,
#         'total_tests': 6,
#         'failed_tests': [
#             {
#                 'suite': 'add function',
#                 'test_case': 'Type case - adding a number and a string',
#                 'passed': False,
#                 'received': None,
#                 'expected': None,
#                 'description': '''add function › Type case - adding a number and a string
# expect(received).rejects.toThrow()

#     Received promise resolved instead of rejected
#     Resolved to value: "32"

#       19 |
#       20 |     test('Type case - adding a number and a string', async () => {
#     > 21 |         await expect(add('3', 2)).rejects.toThrow("3 is not a number");
#          |               ^
#       22 |     });
#       23 |
#       24 |     test('Type case - adding an object', async () => {

#       at expect (../../../../.nvm/versions/node/v20.10.0/lib/node_modules/jest/node_modules/expect/build/index.js:113:15)
#       at Object.expect (utils/temp_jest_vnm8w8qd.test.js:21:15)'''
#             },
#             {
#                 'suite': 'add function',
#                 'test_case': 'Type case - adding an object',
#                 'passed': False,
#                 'received': None,
#                 'expected': None,
#                 'description': '''add function › Type case - adding an object
# expect(received).rejects.toThrow()

#     Received promise resolved instead of rejected
#     Resolved to value: "[object Object]5"

#       23 |
#       24 |     test('Type case - adding an object', async () => {
#     > 25 |         await expect(add({}, 5)).rejects.toThrow("[object Object] is not a number");
#          |               ^
#       26 |     });
#       27 | });

#       at expect (../../../../.nvm/versions/node/v20.10.0/lib/node_modules/jest/node_modules/expect/build/index.js:113:15)
#       at Object.expect (utils/temp_jest_vnm8w8qd.test.js:25:15)'''
#             }
#         ]
#     }

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