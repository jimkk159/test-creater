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
        "thinking": 'The question is asking for the content of the file "myMath.js". Based on the previous action result, I already have the content of that file, which includes a function definition for adding two numbers and the module export statement.\n',
        "tool_result": "function add(a, b) {\n    return a + b;\n}\n\nmodule.exports = { add };\n\n",
        "result": "✅ FILE CONTENT:\nfunction add(a, b) {\n    return a + b;\n}\n\nmodule.exports = { add };",
    },
    "error": {"decide": {}},
    "file_path": "test/myMath.js",
    "analyze": {
        "file_content": "function add(a, b) {\n    return a + b;\n}\n\nmodule.exports = { add };\n\n"
    },
    "functions": {"add": "function add(a, b) {\n    return a + b;\n}"},
    "suggested_file_path": "/Users/jim/test/test-creater/test/_20250618_0315c73.myMath_suggestion.js",
    "generateTestCases": {"add": {}},
    "test_cases": {
        "add": {
            "init": [
                {
                    "name": "Basic case - two positive numbers",
                    "explain": "Testing the addition of two basic positive numbers.",
                    "input": {"a": 5, "b": 10},
                    "expected": 15,
                },
                {
                    "name": "Basic case - negative and positive number",
                    "explain": "Testing the addition of a negative number and a positive number.",
                    "input": {"a": -3, "b": 7},
                    "expected": 4,
                },
                {
                    "name": "Edge case - zero",
                    "explain": "Testing addition of zero with a positive number.",
                    "input": {"a": 0, "b": 10},
                    "expected": 10,
                },
                {
                    "name": "Edge case - zero with negative number",
                    "explain": "Testing addition of zero with a negative number.",
                    "input": {"a": 0, "b": -5},
                    "expected": -5,
                },
                {
                    "name": "Edge case - two zeros",
                    "explain": "Testing the addition of two zero values.",
                    "input": {"a": 0, "b": 0},
                    "expected": 0,
                },
                {
                    "name": "Edge case - large numbers",
                    "explain": "Testing the addition of two large positive numbers.",
                    "input": {"a": 1000000, "b": 2000000},
                    "expected": 3000000,
                },
                {
                    "name": "Edge case - large negative numbers",
                    "explain": "Testing the addition of two large negative numbers.",
                    "input": {"a": -1000000, "b": -2000000},
                    "expected": -3000000,
                },
                {
                    "name": "Input type check - string input",
                    "explain": "Testing the function with string input instead of numbers.",
                    "input": {"a": "5", "b": "10"},
                    "expected": "Error",
                },
                {
                    "name": "Input type check - undefined input",
                    "explain": "Testing the function with undefined as an input.",
                    "input": {"a": "undefined", "b": 10},
                    "expected": "Error",
                },
                {
                    "name": "Input type check - NaN input",
                    "explain": "Testing the function with NaN as an input.",
                    "input": {"a": "NaN", "b": 10},
                    "expected": "Error",
                },
            ]
        }
    },
    "implement": {"add": {}},
    "test_code": {
        "add": "const { add } = require('/Users/jim/test/test-creater/test/myMath.js');\n\ndescribe('add function', () => {\n    test('Basic case - two positive numbers', () => {\n        expect(add(5, 10)).toBe(15);\n    });\n\n    test('Basic case - negative and positive number', () => {\n        expect(add(-3, 7)).toBe(4);\n    });\n\n    test('Edge case - zero', () => {\n        expect(add(0, 10)).toBe(10);\n    });\n\n    test('Edge case - zero with negative number', () => {\n        expect(add(0, -5)).toBe(-5);\n    });\n\n    test('Edge case - two zeros', () => {\n        expect(add(0, 0)).toBe(0);\n    });\n\n    test('Edge case - large numbers', () => {\n        expect(add(1000000, 2000000)).toBe(3000000);\n    });\n\n    test('Edge case - large negative numbers', () => {\n        expect(add(-1000000, -2000000)).toBe(-3000000);\n    });\n\n    test('Input type check - string input', () => {\n        expect(() => add(\"5\", 10)).toThrow(Error);\n    });\n\n    test('Input type check - undefined input', () => {\n        expect(() => add(undefined, 10)).toThrow(Error);\n    });\n\n    test('Input type check - NaN input', () => {\n        expect(() => add(NaN, 10)).toThrow(Error);\n    });\n});"
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
