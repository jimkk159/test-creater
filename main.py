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
    "functions": {
        "add": "function add(a, b) {\n    return a + b;\n}\n",
        "sub": "function sub(a, b) {\n    return a - b;\n}\n",
        "mul": "function mul(a, b) {\n    return a * b;\n}\n",
        "div": "function div(a, b) {\n    return a / b;\n}",
    },
    "functions_order": ["add", "sub", "mul", "div"],
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
