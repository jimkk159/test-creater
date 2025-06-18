import sys
import asyncio
from flow import auto_code_test_generate_flow

BORDER_LEN = 96
border = f"{"=" * BORDER_LEN}"

read_and_find_file_shared = {
    "question": "what is the content in the file myMath.js!",
    "file": {
        "tools": [],
        "tool_info": '[1] read_file_tool\n  Description: Reads the content of a file. \n   Usually you need to check where the target file are located first by tool read_directory_tree_tool\n\nArgs:\n    path: The path to the file.\n    example: "."\n\nReturns:\n    The content of the file as a string.\n\n  Parameters:\n    - path (string): (Required)\n[2] read_directory_tree_tool\n  Description: Reads the recursive directory tree structure of a given path and formats it as a string.\n\nArgs:\n    path: The path to the directory. Defaults to the current directory.\n    indent: Internal parameter for formatting indentation.\n    is_last: Internal parameter to indicate if the current item is the last in its parent directory.\n\nReturns:\n    A string representing the directory tree.\n\n  Parameters:\n    - path (string): (Optional)\n    - indent (string): (Optional)\n    - is_last (boolean): (Optional)',
        "action": "done",
        "tool_name": None,
        "parameters": {},
        "thinking": 'The question asks for the content of the file "myMath.js". Based on the previous action, I already have the content of this file. The content includes two functions, `add` and `sub`, and exports them as a module.\n',
        "tool_result": "function add(a, b) {\n    return a + b;\n}\n\nfunction sub(a, b) {\n    return a - b;\n}\n\nmodule.exports = { add, sub };\n\n",
        "result": "✅ FILE CONTENT:\nfunction add(a, b) {\n    return a + b;\n}\n\nfunction sub(a, b) {\n    return a - b;\n}\n\nmodule.exports = { add, sub };",
    },
    "error": {"decide": {}},
    "file_path": "test/myMath.js",
    "analyze": {
        "file_content": "function add(a, b) {\n    return a + b;\n}\n\nfunction sub(a, b) {\n    return a - b;\n}\n\nmodule.exports = { add, sub };\n\n"
    },
    "functions": {
        "add": "function add(a, b) {\n    return a + b;\n}\n",
        "sub": "function sub(a, b) {\n    return a - b;\n}",
    },
    "suggested_file_path": {
        "add": "/Users/jim/test/test-creater/test/_20250619_83cb486.add_myMath_suggestion.js",
        "sub": "/Users/jim/test/test-creater/test/_20250619_83cb486.sub_myMath_suggestion.js",
    },
    "generateTestCases": {"add": {}, "sub": {}},
    "test_cases": {
        "add": {
            "init": [
                {
                    "name": "Basic case - positive numbers",
                    "explain": "Testing the addition of two positive numbers",
                    "input": {"a": 5, "b": 3},
                    "expected": 8,
                },
                {
                    "name": "Basic case - negative numbers",
                    "explain": "Testing the addition of two negative numbers",
                    "input": {"a": -2, "b": -3},
                    "expected": -5,
                },
                {
                    "name": "Basic case - positive and negative numbers",
                    "explain": "Testing the addition of a positive and a negative number",
                    "input": {"a": 4, "b": -2},
                    "expected": 2,
                },
                {
                    "name": "Edge case - both inputs as zero",
                    "explain": "Testing the addition of zero and zero",
                    "input": {"a": 0, "b": 0},
                    "expected": 0,
                },
                {
                    "name": "Edge case - one input as zero",
                    "explain": "Testing the addition of zero and a positive number",
                    "input": {"a": 0, "b": 10},
                    "expected": 10,
                },
                {
                    "name": "Edge case - large numbers",
                    "explain": "Testing the addition of two very large numbers",
                    "input": {"a": "1e14", "b": "1e14"},
                    "expected": "2e14",
                },
                {
                    "name": "Corner case - type checking with string",
                    "explain": "Testing the function's response to a string input instead of a number",
                    "input": {"a": "5", "b": 3},
                    "expected": "Error: Invalid input type",
                },
                {
                    "name": "Corner case - type checking with boolean",
                    "explain": "Testing the function's response to boolean inputs",
                    "input": {"a": True, "b": False},
                    "expected": "Error: Invalid input type",
                },
                {
                    "name": "Corner case - undefined input",
                    "explain": "Testing the function's response when an input is undefined",
                    "input": {"a": "undefined", "b": 5},
                    "expected": "Error: Invalid input type",
                },
            ]
        },
        "sub": {
            "init": [
                {
                    "name": "Basic case - Positive numbers",
                    "explain": "Test the subtraction of two positive integers.",
                    "input": {"param1": 10, "param2": 4},
                    "expected": 6,
                },
                {
                    "name": "Basic case - Negative and positive number",
                    "explain": "Test the subtraction of a negative integer from a positive integer.",
                    "input": {"param1": 5, "param2": -3},
                    "expected": 8,
                },
                {
                    "name": "Edge case - Subtracting zero",
                    "explain": "Test the subtraction of zero from a positive integer.",
                    "input": {"param1": 10, "param2": 0},
                    "expected": 10,
                },
                {
                    "name": "Edge case - Zero minus a number",
                    "explain": "Test the subtraction of a positive integer from zero.",
                    "input": {"param1": 0, "param2": 5},
                    "expected": -5,
                },
                {
                    "name": "Corner case - Similar numbers",
                    "explain": "Test the subtraction of the same number.",
                    "input": {"param1": 7, "param2": 7},
                    "expected": 0,
                },
                {
                    "name": "Edge case - Large numbers",
                    "explain": "Test the subtraction of two large integers.",
                    "input": {"param1": 1000000, "param2": 999999},
                    "expected": 1,
                },
                {
                    "name": "Input type check - String instead of number",
                    "explain": "Test the function with a string input to see if it handles type errors.",
                    "input": {"param1": "10", "param2": 5},
                    "expected": "Error",
                },
                {
                    "name": "Input type check - Boolean input",
                    "explain": "Test the function with boolean inputs.",
                    "input": {"param1": True, "param2": False},
                    "expected": 1,
                },
            ]
        },
    },
    "implement": {"add": {}, "sub": {}},
    "test_code": {
        "add": "const { add } = require('/Users/jim/test/test-creater/test/myMath.js');\n\ndescribe('add function', () => {\n    test('Basic case - positive numbers', () => {\n        expect(add(5, 3)).toBe(8);\n    });\n\n    test('Basic case - negative numbers', () => {\n        expect(add(-2, -3)).toBe(-5);\n    });\n\n    test('Basic case - positive and negative numbers', () => {\n        expect(add(4, -2)).toBe(2);\n    });\n\n    test('Edge case - both inputs as zero', () => {\n        expect(add(0, 0)).toBe(0);\n    });\n\n    test('Edge case - one input as zero', () => {\n        expect(add(0, 10)).toBe(10);\n    });\n\n    test('Edge case - large numbers', () => {\n        expect(add(1e14, 1e14)).toBe(2e14);\n    });\n\n    test('Corner case - type checking with string', () => {\n        expect(() => add(5, \"3\")).toThrowError(new Error('Invalid input type'));\n    });\n\n    test('Corner case - type checking with boolean', () => {\n        expect(() => add(5, true)).toThrowError(new Error('Invalid input type'));\n    });\n\n    test('Corner case - undefined input', () => {\n        expect(() => add(undefined, 5)).toThrowError(new Error('Invalid input type'));\n    });\n});",
        "sub": "const { sub } = require('/Users/jim/test/test-creater/test/myMath.js');\n\ndescribe('sub', () => {\n    test('Basic case - Positive numbers', () => {\n        expect(sub(10, 4)).toBe(6);\n    });\n\n    test('Basic case - Negative and positive number', () => {\n        expect(sub(5, -3)).toBe(8);\n    });\n\n    test('Edge case - Subtracting zero', () => {\n        expect(sub(10, 0)).toBe(10);\n    });\n\n    test('Edge case - Zero minus a number', () => {\n        expect(sub(0, 5)).toBe(-5);\n    });\n\n    test('Corner case - Similar numbers', () => {\n        expect(sub(7, 7)).toBe(0);\n    });\n\n    test('Edge case - Large numbers', () => {\n        expect(sub(1000000, 999999)).toBe(1);\n    });\n\n    test('Input type check - String instead of number', () => {\n        expect(() => sub(\"10\", 5)).toThrow();\n    });\n\n    test('Input type check - Boolean input', () => {\n        expect(sub(true, false)).toBe(1);\n    });\n});",
    },
    "max_iterations": 3,
    "suite_iterations": {"add": {}, "sub": {"sub": 1}},
    "passed": {"sub": 7},
    "total_tests": {"sub": 8},
    "failed_tests": {
        "sub": [
            {
                "suite": "sub",
                "test_case": "Input type check - String instead of number",
                "passed": False,
                "received": None,
                "expected": None,
                "description": "sub › Input type check - String instead of number\nexpect(received).toThrow()\n\n    Received function did not throw\n\n      27 |\n      28 |     test('Input type check - String instead of number', () => {\n    > 29 |         expect(() => sub(\"10\", 5)).toThrow();\n         |                                    ^\n      30 |     });\n      31 |\n      32 |     test('Input type check - Boolean input', () => {\n\n      at Object.toThrow (test/temp_jest_62ia63bj.test.js:29:36)",
            }
        ]
    },
}


async def main():
    """Runs the Test Code Generator application."""
    print(border)
    print("Starting Test Code Generator...")

    question = "what is the content in the file myMath.js!"

    shared = {
        "question": question,
    }

    # Create and run the flow
    flow = auto_code_test_generate_flow()
    await flow.run_async(read_and_find_file_shared)


if __name__ == "__main__":
    asyncio.run(main())
