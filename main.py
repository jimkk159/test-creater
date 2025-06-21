import sys
import asyncio
from flow import auto_code_test_generate_flow

BORDER_LEN = 96
border = f"{"=" * BORDER_LEN}"

read_and_find_file_shared = {
    "question": "what is the content in the file myMath.js!",
    "file": {
        "tools": [

        ],
        "tool_info": '[1] read_file_tool\n  Description: Reads the content of a file. \n   Usually you need to check where the target file are located first by tool read_directory_tree_tool\n\nArgs:\n    path: The path to the file.\n    example: "."\n\nReturns:\n    The content of the file as a string.\n\n  Parameters:\n    - path (string): (Required)\n[2] read_directory_tree_tool\n  Description: Reads the recursive directory tree structure of a given path and formats it as a string.\n\nArgs:\n    path: The path to the directory. Defaults to the current directory.\n    indent: Internal parameter for formatting indentation.\n    is_last: Internal parameter to indicate if the current item is the last in its parent directory.\n\nReturns:\n    A string representing the directory tree.\n\n  Parameters:\n    - path (string): (Optional)\n    - indent (string): (Optional)\n    - is_last (boolean): (Optional)',
        "action": "done",
        "tool_name": None,
        "parameters": {},
        "thinking": "The question asks for the content of the file myMath.js. \nI have previously read the content of this file and extracted its functions.\nThere is no need for further actions as the content has already been provided.\n",
        "tool_result": "function add(a, b) {\n    return a + b;\n}\n\nfunction sub(a, b) {\n    return a - b;\n}\n\nmodule.exports = { add, sub };\n\n",
        "result": "✅ FILE CONTENT:\nfunction add(a, b) {\n    return a + b;\n}\n\nfunction sub(a, b) {\n    return a - b;\n}\n\nmodule.exports = { add, sub };",
    },
    "error": {"decide": {}},
    "file_path": "test/myMath.js",
    "analyze": {
        "file_content": "function add(a, b) {\n    return a + b;\n}\n\nfunction sub(a, b) {\n    return a - b;\n}\n\nmodule.exports = { add, sub };\n\n"
    },
    "functions": {
        "add": "function add(a, b) {\n    if (typeof a !== 'number' || typeof b !== 'number') {\n        throw new Error(\"Invalid input: both parameters must be numbers.\");\n    }\n    return a + b;\n}\n\nmodule.exports = { add };\n",
        "sub": "function sub(a, b) {\n    return a - b;\n}",
    },
    "functions_order": ["add", "sub"],
    "suggested_file_path": {
        "add": "/Users/jim/test/test-creater/test/_20250621_7bf60e3.add_myMath_suggestion.js",
        "sub": "/Users/jim/test/test-creater/test/_20250621_7bf60e3.sub_myMath_suggestion.js",
    },
    "generateTestCases": {"add": {}, "sub": {}},
    "test_cases": {
        "add": {
            "init": [
                {
                    "name": "Basic case - positive numbers",
                    "explain": "Testing basic functionality with two positive integers.",
                    "input": {"a": 5, "b": 3},
                    "expected": 8,
                },
                {
                    "name": "Basic case - mix of positive and negative numbers",
                    "explain": "Testing addition with one positive and one negative integer.",
                    "input": {"a": 7, "b": -2},
                    "expected": 5,
                },
                {
                    "name": "Edge case - zero value",
                    "explain": "Testing addition of a number with zero to check correct output.",
                    "input": {"a": 0, "b": 10},
                    "expected": 10,
                },
                {
                    "name": "Edge case - both zeros",
                    "explain": "Testing addition of two zero values.",
                    "input": {"a": 0, "b": 0},
                    "expected": 0,
                },
                {
                    "name": "Corner case - large numbers",
                    "explain": "Testing addition with large integer values to check for overflow.",
                    "input": {"a": 1000000000, "b": 2000000000},
                    "expected": 3000000000,
                },
                {
                    "name": "Corner case - negative large numbers",
                    "explain": "Testing addition with large negative integers.",
                    "input": {"a": -1000000000, "b": -2000000000},
                    "expected": -3000000000,
                },
                {
                    "name": "Input type check - string input",
                    "explain": "Testing behavior when non-numeric input is provided.",
                    "input": {"a": "five", "b": 5},
                    "expected": "Error",
                },
                {
                    "name": "Input type check - boolean input",
                    "explain": "Testing behavior when boolean inputs are provided.",
                    "input": {"a": True, "b": False},
                    "expected": 1,
                },
                {
                    "name": "Input type check - undefined",
                    "explain": "Testing behavior when one parameter is undefined.",
                    "input": {"a": "undefined", "b": 5},
                    "expected": "Error",
                },
            ]
        },
        "sub": {
            "init": [
                {
                    "name": "Basic case - positive numbers",
                    "explain": "Testing with two positive integers to verify basic subtraction functionality.",
                    "input": {"a": 10, "b": 5},
                    "expected": 5,
                },
                {
                    "name": "Basic case - negative and positive number",
                    "explain": "Testing with a negative integer and a positive integer to ensure correct handling of signs.",
                    "input": {"a": -3, "b": 7},
                    "expected": -10,
                },
                {
                    "name": "Edge case - zero",
                    "explain": "Testing with zero as the first parameter to see if it handles subtraction correctly.",
                    "input": {"a": 0, "b": 5},
                    "expected": -5,
                },
                {
                    "name": "Edge case - zero as second parameter",
                    "explain": "Testing with zero as the second parameter to confirm that the function returns the first parameter.",
                    "input": {"a": 5, "b": 0},
                    "expected": 5,
                },
                {
                    "name": "Edge case - both parameters are zero",
                    "explain": "Testing when both parameters are zero to ensure it returns zero.",
                    "input": {"a": 0, "b": 0},
                    "expected": 0,
                },
                {
                    "name": "Edge case - larger first parameter",
                    "explain": "Testing with a larger first parameter to ensure positive results are returned correctly.",
                    "input": {"a": 100, "b": 50},
                    "expected": 50,
                },
                {
                    "name": "Edge case - larger second parameter",
                    "explain": "Testing with a pre-negatively large second parameter to verify it gives a positive result.",
                    "input": {"a": 50, "b": 100},
                    "expected": -50,
                },
                {
                    "name": "Corner case - very large numbers",
                    "explain": "Testing with very large positive numbers to ensure function performance and correctness.",
                    "input": {"a": 1000000, "b": 500000},
                    "expected": 500000,
                },
                {
                    "name": "Corner case - very large negative numbers",
                    "explain": "Testing with very large negative numbers to ensure the function correctly processes them.",
                    "input": {"a": -1000000, "b": -500000},
                    "expected": -500000,
                },
                {
                    "name": "Type check case - string input",
                    "explain": "Testing with incorrect types (string) to confirm that function handles type errors gracefully.",
                    "input": {"a": "ten", "b": 5},
                    "expected": "NaN",
                },
                {
                    "name": "Type check case - boolean input",
                    "explain": "Testing with boolean values to check if the function converts them correctly.",
                    "input": {"a": True, "b": False},
                    "expected": 1,
                },
            ]
        },
    },
    "implement": {"add": {}, "sub": {}},
    "test_code": {
        "add": "const { add } = require('/Users/jim/test/test-creater/test/_20250621_7bf60e3.add_myMath_suggestion.js');\n\ndescribe('add', () => {\n    test('Basic case - positive numbers', () => {\n        expect(add(5, 3)).toBe(8);\n    });\n\n    test('Basic case - mix of positive and negative numbers', () => {\n        expect(add(7, -2)).toBe(5);\n    });\n\n    test('Edge case - zero value', () => {\n        expect(add(0, 10)).toBe(10);\n    });\n\n    test('Edge case - both zeros', () => {\n        expect(add(0, 0)).toBe(0);\n    });\n\n    test('Corner case - large numbers', () => {\n        expect(add(1000000000, 2000000000)).toBe(3000000000);\n    });\n\n    test('Corner case - negative large numbers', () => {\n        expect(add(-1000000000, -2000000000)).toBe(-3000000000);\n    });\n\n    test('Input type check - string input', () => {\n        expect(() => add('five', 5)).toThrow(Error);\n    });\n\n    test('Input type check - boolean input', () => {\n        expect(() => add(true, false)).toThrow(Error);\n    });\n\n    test('Input type check - undefined', () => {\n        expect(() => add(undefined, 5)).toThrow(Error);\n    });\n});",
        "sub": "const { sub } = require('/Users/jim/test/test-creater/test/myMath.js');\n\ndescribe('sub function', () => {\n    test('Basic case - positive numbers', () => {\n        expect(sub(10, 5)).toBe(5);\n    });\n\n    test('Basic case - negative and positive number', () => {\n        expect(sub(-3, 7)).toBe(-10);\n    });\n\n    test('Edge case - zero', () => {\n        expect(sub(0, 5)).toBe(-5);\n    });\n\n    test('Edge case - zero as second parameter', () => {\n        expect(sub(5, 0)).toBe(5);\n    });\n\n    test('Edge case - both parameters are zero', () => {\n        expect(sub(0, 0)).toBe(0);\n    });\n\n    test('Edge case - larger first parameter', () => {\n        expect(sub(100, 50)).toBe(50);\n    });\n\n    test('Edge case - larger second parameter', () => {\n        expect(sub(50, 100)).toBe(-50);\n    });\n\n    test('Corner case - very large numbers', () => {\n        expect(sub(1000000, 500000)).toBe(500000);\n    });\n\n    test('Corner case - very large negative numbers', () => {\n        expect(sub(-1000000, -500000)).toBe(-500000);\n    });\n\n    test('Type check case - string input', () => {\n        expect(sub('ten', 5)).toBeNaN();\n    });\n\n    test('Type check case - boolean input', () => {\n        expect(sub(true, false)).toBe(1);\n    });\n});",
    },
    "max_iterations": 3,
    "suite_iterations": {"add": {"add": 3}, "sub": {"sub function": 1}},
    "passed": {"add": 8},
    "total_tests": {"add": 9},
    "failed_tests": {
        "add": [
            {
                "suite": "add",
                "test_case": "Input type check - boolean input",
                "passed": False,
                "received": None,
                "expected": None,
                "description": "add › Input type check - boolean input\nInvalid input: both parameters must be numbers.\n\n      1 | function add(a, b) {\n      2 |     if (typeof a !== 'number' || typeof b !== 'number') {\n    > 3 |         throw new Error(\"Invalid input: both parameters must be numbers.\");\n        |               ^\n      4 |     }\n      5 |     return a + b;\n      6 | }\n\n      at add (test/_20250621_7bf60e3.add_myMath_suggestion.js:3:15)\n      at Object.add (test/temp_jest__208o9kh.test.js:33:16)",
            }
        ]
    },
    "iteration_count": {"add": 2},
    "revise": {"add": {}},
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
    await flow.run_async(shared)


if __name__ == "__main__":
    asyncio.run(main())
