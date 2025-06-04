from fastmcp import FastMCP
import os

# Create a named server
mcp = FastMCP("Math Operations Server")

# Define mathematical operation tools
@mcp.tool()
def read_file_tool(path: str) -> str:
    """Reads the content of a file. 
       Usually you need to check where the target file are located first by tool read_directory_tree_tool

    Args:
        path: The path to the file.
        example: "."

    Returns:
        The content of the file as a string.
    """
    try:
        with open(path, 'r') as f:
            content = f.read()
        return content
    except Exception as e:
        return f"Error reading file: {e}"

@mcp.tool()
def read_directory_tree_tool(path: str = '.', indent: str = '', is_last: bool = True) -> str:
    """Reads the recursive directory tree structure of a given path and formats it as a string.

    Args:
        path: The path to the directory. Defaults to the current directory.
        indent: Internal parameter for formatting indentation.
        is_last: Internal parameter to indicate if the current item is the last in its parent directory.

    Returns:
        A string representing the directory tree.
    """
    output = ""
    if indent == '':
        output += f"Directory structure for {os.path.basename(path)}:\n"

    try:
        entries = os.listdir(path)
        # Filter out hidden files/directories and sort
        entries = sorted([e for e in entries if not e.startswith('.')])

        for i, entry in enumerate(entries):
            is_current_last = (i == len(entries) - 1)
            # Choose the correct prefix based on whether it's the last item
            prefix = "└── " if is_current_last else "├── "
            output += f"{indent}{prefix}{entry}\n"

            entry_path = os.path.join(path, entry)
            if os.path.isdir(entry_path):
                # Calculate the indentation for the recursive call
                next_indent = indent + ("    " if is_last else "│   ")
                output += read_directory_tree_tool(entry_path, next_indent, is_current_last)

    except FileNotFoundError:
        return output + f"{indent}Error: Directory not found at {path}\n"
    except Exception as e:
        return output + f"{indent}Error reading directory {path}: {e}\n"

    return output

# Start the server
if __name__ == "__main__":
    mcp.run()