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
        "thinking": 'The question asks for the content of the file "myMath.js". I have already retrieved the content of that file in the previous action, which contains JavaScript functions for basic arithmetic operations. Since I have the answer ready, there is no further action needed.\n',
        "tool_result": "function add(a, b) {\n    return a + b;\n}\n\nfunction sub(a, b) {\n    return a - b;\n}\n\nfunction mul(a, b) {\n    return a * b;\n}\n\nfunction div(a, b) {\n    return a / b;\n}\n\nmodule.exports = { add, sub, mul, div };\n\n",
        "result": "✅ FILE CONTENT:\nfunction add(a, b) {\n    return a + b;\n}\n\nfunction sub(a, b) {\n    return a - b;\n}\n\nfunction mul(a, b) {\n    return a * b;\n}\n\nfunction div(a, b) {\n    return a / b;\n}\n\nmodule.exports = { add, sub, mul, div };",
    },
    "error": {"decide": {}},
    "file_path": "myMath.js",
    "analyze": {
        "file_content": "function add(a, b) {\n    return a + b;\n}\n\nfunction sub(a, b) {\n    return a - b;\n}\n\nfunction mul(a, b) {\n    return a * b;\n}\n\nfunction div(a, b) {\n    return a / b;\n}\n\nmodule.exports = { add, sub, mul, div };\n\n"
    },
    "functions": {"add": "function add(a, b) {\n    return a + b;\n}\n"},
    "functions_order": ["add"],
    "suggested_file_path": {
        "add": "/Users/jim/test/test-creater/test/_20250621_6ea4750.add_myMath_suggestion.js"
    },
    "generateTestCases": {"add": {}},
    "test_cases": {
        "add": {
            "init": [
                {
                    "name": "Basic case - two positive integers",
                    "explain": "Testing the addition of two positive integers to verify basic functionality.",
                    "input": {"param1": 5, "param2": 10},
                    "expected": 15,
                },
                {
                    "name": "Basic case - positive and negative integer",
                    "explain": "Testing the addition of a positive integer and a negative integer to check if it handles mixed signs correctly.",
                    "input": {"param1": 7, "param2": -3},
                    "expected": 4,
                },
                {
                    "name": "Basic case - two negative integers",
                    "explain": "Testing the addition of two negative integers to see if it returns the correct result.",
                    "input": {"param1": -5, "param2": -10},
                    "expected": -15,
                },
                {
                    "name": "Edge case - zero",
                    "explain": "Testing the addition of zero to another number to check if it returns the other number.",
                    "input": {"param1": 0, "param2": 10},
                    "expected": 10,
                },
                {
                    "name": "Edge case - very large numbers",
                    "explain": "Testing the addition of very large numbers to verify that the function can handle them without overflow.",
                    "input": {"param1": "1e12", "param2": "1e12"},
                    "expected": "2e12",
                },
                {
                    "name": "Edge case - very small numbers",
                    "explain": "Testing the addition of very small numbers to verify that the function can handle them accurately.",
                    "input": {"param1": "1e-12", "param2": "1e-12"},
                    "expected": "2e-12",
                },
                {
                    "name": "Corner case - both parameters are zero",
                    "explain": "Testing the addition of zero with zero to verify the function outputs zero as expected.",
                    "input": {"param1": 0, "param2": 0},
                    "expected": 0,
                },
                {
                    "name": "Input type check - string inputs",
                    "explain": "Testing the function with invalid string inputs to ensure it handles type errors gracefully.",
                    "input": {"param1": "a", "param2": "b"},
                    "expected": "Error",
                },
                {
                    "name": "Input type check - mixed types",
                    "explain": "Testing the function with one number and one string input to see how it handles invalid input types.",
                    "input": {"param1": 5, "param2": "b"},
                    "expected": "Error",
                },
            ]
        }
    },
}

revise_shared = {
    "question": "what is the content in the file myMath.js!",
    "file": {
        "tools": [],
        "tool_info": '[1] read_file_tool\n  Description: Reads the content of a file. \n   Usually you need to check where the target file are located first by tool read_directory_tree_tool\n\nArgs:\n    path: The path to the file.\n    example: "."\n\nReturns:\n    The content of the file as a string.\n\n  Parameters:\n    - path (string): (Required)\n[2] read_directory_tree_tool\n  Description: Reads the recursive directory tree structure of a given path and formats it as a string.\n\nArgs:\n    path: The path to the directory. Defaults to the current directory.\n    indent: Internal parameter for formatting indentation.\n    is_last: Internal parameter to indicate if the current item is the last in its parent directory.\n\nReturns:\n    A string representing the directory tree.\n\n  Parameters:\n    - path (string): (Optional)\n    - indent (string): (Optional)\n    - is_last (boolean): (Optional)',
        "action": "done",
        "tool_name": None,
        "parameters": {},
        "thinking": 'The question asks for the content of the file "myMath.js". \nBased on the previous action, I already have the content of the file, which is the implementation of a simple addition function in JavaScript.\n',
        "tool_result": "function add(a, b) {\n    return a + b;\n}\nmodule.exports = { add };\n\n",
        "result": "✅ FILE CONTENT:\nfunction add(a, b) {\n    return a + b;\n}\nmodule.exports = { add };",
    },
    "error": {"decide": {}},
    "file_path": "myMath.js",
    "analyze": {
        "file_content": "function add(a, b) {\n    return a + b;\n}\nmodule.exports = { add };\n\n"
    },
    "functions": {
        "add": "const { isNaN } = require('core-js/library/fn/typeof');\n\nfunction add(a, b) {\n    // If parameters are numbers or can be converted to numbers\n    if (typeof a === 'string' || typeof b === 'string') {\n        a = Number(a);\n        b = Number(b);\n    }\n\n    // Check for valid numbers after conversion\n    if (typeof a !== 'number' || typeof b !== 'number' || isNaN(a) || isNaN(b)) {\n        return NaN;\n    }\n    return a + b;\n}\n\nmodule.exports = { add };\n"
    },
    "functions_order": ["add"],
    "suggestion": {
        "add": [
            '- name: "Basic case - negative numbers"\n  reason: To ensure correctness of adding two negative numbers.\n  input: {param1: -5, param2: -3}\n  expected: -8\n\n- name: "Basic case - positive and float"\n  reason: To test combining a positive whole number with a floating-point number.\n  input: {param1: 5, param2: 2.5}\n  expected: 7.5\n\n- name: "Input type check - string input representing a number"\n  reason: To specify behavior when a string representing a number is provided.\n  input: {param1: "5", param2: "3"}\n  expected: 8\n\n- name: "Input type check - boolean input"\n  reason: To verify how boolean values are treated in addition.\n  input: {param1: true, param2: 1}\n  expected: 2',
            '- name: "Input type check - string input representing a number"\n  reason: To properly verify behavior when a string representing a number is provided.\n  input: {param1: "5", param2: "3"}\n  expected: 8\n  \n- name: "Error case - object input"\n  reason: To check how the function handles an object as input, which should throw an error or return NaN.\n  input: {param1: {}, param2: 1}\n  expected: NaN\n\n- name: "Error case - array input"\n  reason: To test how the function behaves when an array is provided as input, potentially resulting in concatenation or an unexpected output.\n  input: {param1: [1, 2], param2: 1}\n  expected: "1,21" # Assuming JavaScript would concatenate the array with the number in this situation.',
            '- name: "Input type check - correct string inputs"\n  reason: To ensure the function correctly handles string inputs representing numbers.\n  input: {param1: "5", param2: "3"}\n  expected: 8\n\n- name: "Input type check - incorrect string inputs"\n  reason: To verify behavior when two non-numeric strings are added.\n  input: {param1: "apple", param2: "banana"}\n  expected: "applebanana"\n\n- name: "Input type check - boolean as false with number"\n  reason: To confirm that boolean value of false is treated correctly when added to a number.\n  input: {param1: false, param2: 5}\n  expected: 5',
            '- name: "Input type check - string input representing a number"\n  reason: To ensure the function correctly handles numeric strings (deduplication).\n  input: {param1: "5", param2: "3"}\n  expected: 8\n  \n- name: "Input type check - boolean input true"\n  reason: To confirm the handling of boolean value true correctly.\n  input: {param1: true, param2: 1}\n  expected: 2\n\n- name: "Input type check - array input correction"\n  reason: To ensure that behavior when an array is added is correctly handled (concatenation and result check).\n  input: {param1: [1, 2], param2: 1}\n  expected: "1,21"\n\n- name: "Input type check - null inputs"\n  reason: To check how the function reacts to `null` inputs.\n  input: {param1: null, param2: 5}\n  expected: 5\n\n- name: "Input type check - undefined inputs"\n  reason: To test behavior when `undefined` is given as input.\n  input: {param1: undefined, param2: 5}\n  expected: "undefined5"',
        ]
    },
    "generateTestCases": {"add": {}},
    "test_cases": {
        "add": {
            "init": [
                {
                    "name": "Basic case - negative numbers",
                    "explain": "To ensure correctness of adding two negative numbers.",
                    "input": {"param1": -5, "param2": -3},
                    "expected": -8,
                },
                {
                    "name": "Basic case - positive and float",
                    "explain": "To test combining a positive whole number with a floating-point number.",
                    "input": {"param1": 5, "param2": 2.5},
                    "expected": 7.5,
                },
                {
                    "name": "Input type check - string input representing a number",
                    "explain": "To specify behavior when a string representing a number is provided.",
                    "input": {"param1": "5", "param2": "3"},
                    "expected": 8,
                },
                {
                    "name": "Input type check - boolean input",
                    "explain": "To verify how boolean values are treated in addition.",
                    "input": {"param1": True, "param2": 1},
                    "expected": 2,
                },
                {
                    "name": "Error case - object input",
                    "explain": "To check how the function handles an object as input, which should throw an error or return NaN.",
                    "input": {"param1": {}, "param2": 1},
                    "expected": "NaN",
                },
                {
                    "name": "Error case - array input",
                    "explain": "To test how the function behaves when an array is provided as input, potentially resulting in concatenation or an unexpected output.",
                    "input": {"param1": [1, 2], "param2": 1},
                    "expected": "1,21",
                },
                {
                    "name": "Input type check - incorrect string inputs",
                    "explain": "To verify behavior when two non-numeric strings are added.",
                    "input": {"param1": "apple", "param2": "banana"},
                    "expected": "applebanana",
                },
                {
                    "name": "Input type check - boolean as false with number",
                    "explain": "To confirm that a boolean value of false is treated correctly when added to a number.",
                    "input": {"param1": False, "param2": 5},
                    "expected": 5,
                },
            ]
        }
    },
    "suggestion_iteration_count": {"add": 4},
    "implement": {"add": {}},
    "test_code": {
        "add": "const { add } = require('/Users/jim/test/test-creater/test/_20250622_6ea4750.add_myMath_suggestion.js');\n\ndescribe('add function', () => {\n    test('Basic case - negative numbers', () => {\n        expect(add(-5, -3)).toBe(-8);\n    });\n\n    test('Basic case - positive and float', () => {\n        expect(add(5, 2.5)).toBe(7.5);\n    });\n\n    test('Input type check - string input representing a number', () => {\n        expect(add(\"5\", \"3\")).toBe(8);\n    });\n\n    test('Input type check - boolean input', () => {\n        expect(add(true, 1)).toBe(2);\n    });\n\n    test('Error case - object input', () => {\n        expect(isNaN(add({}, 1))).toBe(true); \n    });\n\n    test('Error case - array input', () => {\n        expect(isNaN(add([1, 2], 1))).toBe(true);\n    });\n\n    test('Input type check - incorrect string inputs', () => {\n        expect(isNaN(add(\"apple\", \"banana\"))).toBe(true);\n    });\n\n    test('Input type check - boolean as false with number', () => {\n        expect(add(false, 5)).toBe(5);\n    });\n});"
    },
    "max_iteration": 5,
    "suite_iterations": {"add": {"add function": 6}},
    "passed": {"add": 6},
    "total_tests": {"add": 8},
    "failed_tests": {
        "add": [
            {
                "suite": "add function",
                "test_case": "Input type check - string input representing a number",
                "passed": False,
                "received": '"53"',
                "expected": "8",
                "description": "add function › Input type check - string input representing a number\n11 |\n      12 |     test('Input type check - string input representing a number', () => {\n    > 13 |         expect(add(\"5\", \"3\")).toBe(8); // assuming the input should be treated as numbers\n         |                               ^\n      14 |     });\n      15 |\n      16 |     test('Input type check - boolean input', () => {\n\n      at Object.toBe (test/temp_jest_br3yahc0.test.js:13:31)",
            },
            {
                "suite": "add function",
                "test_case": "Error case - object input",
                "passed": False,
                "received": '"[object Object]1"',
                "expected": None,
                "description": "add function › Error case - object input\n19 |\n      20 |     test('Error case - object input', () => {\n    > 21 |         expect(add({}, 1)).toBeNaN(); // {} + 1 results in NaN\n         |                            ^\n      22 |     });\n      23 |\n      24 |     test('Error case - array input', () => {\n\n      at Object.toBeNaN (test/temp_jest_br3yahc0.test.js:21:28)",
            },
        ]
    },
    "iteration_count": {"add": 5},
    "suggested_file_path": {
        "add": "/Users/jim/test/test-creater/test/_20250622_6ea4750.add_myMath_suggestion.js"
    },
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
