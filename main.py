import sys
import asyncio
from flow import auto_code_test_generate_flow

BORDER_LEN = 96
border = f"{"=" * BORDER_LEN}"

read_and_find_file_shared = {
    "error": {"decide": {}},
    "file": {
        "action": "done",
        "parameters": {},
        "result": "",
        "thinking": "",
        "tool_info": "",
        "tool_name": None,
        "tool_result": "function add(a, b) {\n"
        "    return a + b;\n"
        "}\n"
        "\n"
        "module.exports = { add };\n"
        "\n",
        "tools": [],
    },
    "file_path": "test/myMath_suggestion.js",
    "question": "what is the content in the file myMath.js!",
    "analyze": {
        "file_content": "function add(a, b) {\n    return a + b;\n}\n\nmodule.exports = { add };\n\n"
    },
    "functions": {"add": "function add(a, b) {\n    return a + b;\n}"},
    "test_cases": {
        "add": {
            "init": [
                {
                    "name": "Basic case - adding two positive numbers",
                    "explain": "Testing the addition of two positive integers.",
                    "input": {"param1": 5, "param2": 7},
                    "expected": 12,
                },
                {
                    "name": "Basic case - adding a positive and a negative number",
                    "explain": "Testing the addition of a positive integer and a negative integer.",
                    "input": {"param1": 10, "param2": -3},
                    "expected": 7,
                },
                {
                    "name": "Edge case - adding zero",
                    "explain": "Testing the addition of a number with zero.",
                    "input": {"param1": 15, "param2": 0},
                    "expected": 15,
                },
                {
                    "name": "Edge case - adding two zeros",
                    "explain": "Testing the addition of zero with zero.",
                    "input": {"param1": 0, "param2": 0},
                    "expected": 0,
                },
                {
                    "name": "Edge case - adding two negative numbers",
                    "explain": "Testing the addition of two negative integers.",
                    "input": {"param1": -4, "param2": -6},
                    "expected": -10,
                },
                {
                    "name": "Corner case - adding large numbers",
                    "explain": "Testing the addition of two large positive integers.",
                    "input": {"param1": 1000000, "param2": 2000000},
                    "expected": 3000000,
                },
                {
                    "name": "Input type check - adding a string and a number",
                    "explain": "Testing behavior when the first input is a string.",
                    "input": {"param1": "5", "param2": 3},
                    "expected": "TypeError",
                },
                {
                    "name": "Input type check - adding a null value",
                    "explain": "Testing behavior when one of the inputs is null.",
                    "input": {"param1": None, "param2": 5},
                    "expected": "TypeError",
                },
                {
                    "name": "Input type check - adding undefined values",
                    "explain": "Testing behavior when one of the inputs is undefined.",
                    "input": {"param1": "undefined", "param2": 7},
                    "expected": "TypeError",
                },
            ]
        }
    },
    "test_code": {
        "add": "const { add } = require('/Users/jimchung/Desktop/Code/python/test-creater/test/myMath.js');\n\ndescribe('add', () => {\n    test('Basic case - adding two positive numbers', () => {\n        expect(add(5, 7)).toBe(12);\n    });\n\n    test('Basic case - adding a positive and a negative number', () => {\n        expect(add(10, -3)).toBe(7);\n    });\n\n    test('Edge case - adding zero', () => {\n        expect(add(15, 0)).toBe(15);\n    });\n\n    test('Edge case - adding two zeros', () => {\n        expect(add(0, 0)).toBe(0);\n    });\n\n    test('Edge case - adding two negative numbers', () => {\n        expect(add(-4, -6)).toBe(-10);\n    });\n\n    test('Corner case - adding large numbers', () => {\n        expect(add(1000000, 2000000)).toBe(3000000);\n    });\n\n    test('Input type check - adding a string and a number', () => {\n        expect(() => add('5', 3)).toThrow(TypeError);\n    });\n\n    test('Input type check - adding a null value', () => {\n        expect(() => add(null, 5)).toThrow(TypeError);\n    });\n\n    test('Input type check - adding undefined values', () => {\n        expect(() => add(undefined, 7)).toThrow(TypeError);\n    });\n});"
    },
    "max_iterations": 5,
    "suite_iterations": {"add": {"add": 1}},
    "passed": {"add": 6},
    "total_tests": {"add": 9},
    "failed_tests": {
        "add": [
            {
                "suite": "add",
                "test_case": "Input type check - adding a string and a number",
                "passed": False,
                "received": None,
                "expected": None,
                "description": "add › Input type check - adding a string and a number\nexpect(received).toThrow(expected)\n\n    Expected constructor: TypeError\n\n    Received function did not throw\n\n      27 |\n      28 |     test('Input type check - adding a string and a number', () => {\n    > 29 |         expect(() => add('5', 3)).toThrow(TypeError);\n         |                                   ^\n      30 |     });\n      31 |\n      32 |     test('Input type check - adding a null value', () => {\n\n      at Object.toThrow (test/temp_jest_3r8rh0re.test.js:29:35)",
            },
            {
                "suite": "add",
                "test_case": "Input type check - adding a null value",
                "passed": False,
                "received": None,
                "expected": None,
                "description": "add › Input type check - adding a null value\nexpect(received).toThrow(expected)\n\n    Expected constructor: TypeError\n\n    Received function did not throw\n\n      31 |\n      32 |     test('Input type check - adding a null value', () => {\n    > 33 |         expect(() => add(null, 5)).toThrow(TypeError);\n         |                                    ^\n      34 |     });\n      35 |\n      36 |     test('Input type check - adding undefined values', () => {\n\n      at Object.toThrow (test/temp_jest_3r8rh0re.test.js:33:36)",
            },
            {
                "suite": "add",
                "test_case": "Input type check - adding undefined values",
                "passed": False,
                "received": None,
                "expected": None,
                "description": "add › Input type check - adding undefined values\nexpect(received).toThrow(expected)\n\n    Expected constructor: TypeError\n\n    Received function did not throw\n\n      35 |\n      36 |     test('Input type check - adding undefined values', () => {\n    > 37 |         expect(() => add(undefined, 7)).toThrow(TypeError);\n         |                                         ^\n      38 |     });\n      39 | });\n\n      at Object.toThrow (test/temp_jest_3r8rh0re.test.js:37:41)",
            },
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
