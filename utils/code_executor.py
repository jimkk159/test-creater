import io
import re
import sys
import traceback
from contextlib import redirect_stdout, redirect_stderr
import os
import tempfile
import subprocess
import asyncio

def extract_failed_tests(jest_output):
    overall_summary = ""
    final_summary = ""
    individual_failures_raw = []

    # Find the start of the final summary block (lines starting with "Test Suites:")
    final_summary_index = jest_output.rfind("Test Suites:")

    if final_summary_index != -1:
        # Extract the final summary block
        final_summary = jest_output[final_summary_index:].strip()
        # The rest of the output contains the initial summary and individual failures
        intermediate_output = jest_output[:final_summary_index].strip()
    else:
        # If the final summary block is not found, the whole output is intermediate
        intermediate_output = jest_output.strip()

    # First try to split by bullet points for regular test failures
    test_failures_split = re.split(r"\n\s*● ", intermediate_output)
    
    if len(test_failures_split) > 1:
        # The first element is the initial overall summary (if any)
        overall_summary = test_failures_split[0].strip()
        # The rest are individual failures
        individual_failures_raw = test_failures_split[1:]
    else:
        # If no bullet points found, check for module resolution errors
        module_error_match = re.search(r"Cannot find module.*?\n", intermediate_output)
        if module_error_match:
            # Extract the module error as a single failure
            individual_failures_raw = [intermediate_output]
            overall_summary = ""

    results = []

    for failure in individual_failures_raw:  # Process individual failures
        # For module resolution errors, use the whole error as description
        if "Cannot find module" in failure:
            results.append({
                "suite": "Module Resolution",
                "test_case": "Import",
                "expected": None,
                "received": None,
                "description": failure.strip()
            })
            continue

        # Extract suite and test name and the rest of the failure output
        header_match = re.match(r"(.*?) › (.*?)\n", failure)
        if not header_match:
            continue

        suite, test = header_match.groups()
        
        # Find the index of the line containing "Received:"
        received_line_end_index = failure.find("Received:")
        description_content = ""

        if received_line_end_index != -1:
            # Find the end of the "Received:" line (the first newline after "Received:")
            end_of_received_line = failure.find('\n', received_line_end_index)
            if end_of_received_line != -1:
                # Take everything after the newline following the "Received:" line
                description_content = failure[end_of_received_line + 1:].strip()
            else:
                 # Handle case where "Received:" is the last line (unlikely but safe)
                 description_content = ""
        else:
            # If "Received:" is not found, use the whole failure block after the header
            # Find the end of the header line
            end_of_header_line = failure.find('\n')
            if end_of_header_line != -1:
                 description_content = failure[end_of_header_line + 1:].strip()

        # Extract Expected and Received values (still needed for separate fields)
        expected_match = re.search(r"Expected:\s+(.*?)\n", failure)
        received_match = re.search(r"Received:\s+(.*?)\n", failure)

        expected = expected_match.group(1).strip() if expected_match else None
        received = received_match.group(1).strip() if received_match else None

        # Construct the description using the header and the content after "Received:"
        full_description = f"{suite} › {test}\n{description_content}".strip()

        results.append({
            "suite": suite,
            "test_case": test,
            "expected": expected,
            "received": received,
            "description": full_description
        })

    # Return the initial summary, final summary, and the list of failures
    return {
        "start": overall_summary,
        "end": final_summary,
        "details": results
    }

def execute_python(function_code, input):
    try:
        namespace = {"__builtins__": __builtins__}
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()
        
        with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
            exec(function_code, namespace)
            
            if "run_code" not in namespace:
                return None, "Function 'run_code' not found"
            
            run_code = namespace["run_code"]
            
            if isinstance(input, dict):
                result = run_code(**input)
            elif isinstance(input, (list, tuple)):
                result = run_code(*input)
            else:
                result = run_code(input)
            
            return result, None
                
    except Exception as e:
        return None, f"{type(e).__name__}: {str(e)}"
    
def create_jest_test_file(test_code):
    """
    Writes JavaScript test code to a temporary file and returns the file path 
    and the command to run it with Jest.
    """
    try:
        # Create a temporary file with .test.js extension
        # delete=False means the file is not deleted when closed, so Jest can access it
        project_dir = os.path.abspath(os.path.dirname(__file__))  # current script dir

        # Use tempfile.mkstemp() to create a secure temporary file
        fd, temp_path = tempfile.mkstemp(prefix='temp_jest_', suffix='.test.js', dir=project_dir)

        # Close the file descriptor immediately as we only need the path
        # Jest will open the file itself later.
        os.close(fd)
        
        # Write the test code to the temporary file
        with open(temp_path, 'w', encoding='utf-8') as tmp_file:
            tmp_file.write(test_code)

        # Construct the command to run Jest on the temp_path file using npx
        command = f"jest --runTestsByPath {temp_path}"

        # Return the path and the command. The calling Node will execute the command.
        return temp_path, command, None
        
    except Exception as e:
        # Return None for path and command, and include the error message
        return None, None, f"Error preparing JS execution: {str(e)}"

async def execute_jest_test(test_code):
    file_path, command, error = create_jest_test_file(test_code)

    if error:
        print(f"Error preparing JS execution: {error}")
    else:
        try:
            # Create async subprocess
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            # Wait for process to complete and get output
            stdout, stderr = await process.communicate()

            # Decode the output
            stdout = stdout.decode('utf-8') if stdout else ""
            stderr = stderr.decode('utf-8') if stderr else ""
                        
            if process.returncode == 0:
                return extract_failed_tests(stderr)
            else:
                return extract_failed_tests(stderr)
                
        except FileNotFoundError:
            return "Error: Jest or npx command not found..."
        except Exception as e:
            print(e)
            return f"An unexpected error occurred: {e}"
        finally:
            if os.path.exists(file_path):
                os.remove(file_path)

def extract_test_counts(test_output_string):
    # Find both Test Suites and Tests lines
    suites_line_match = re.search(r'^Test Suites:\s+(.*)$', test_output_string, re.MULTILINE)
    tests_line_match = re.search(r'^Tests:\s+(.*)$', test_output_string, re.MULTILINE)
    
    suited_failed_count = failed_count = passed_count = total_count = 0

    if suites_line_match:
        suites_line = suites_line_match.group(1)
        suite_failed_match = re.search(r'(\d+)\s+failed', suites_line)
        if suite_failed_match:
            suited_failed_count = int(suite_failed_match.group(1))

    if tests_line_match:
        tests_line = tests_line_match.group(1)

        failed_match = re.search(r'(\d+)\s+failed', tests_line)
        passed_match = re.search(r'(\d+)\s+passed', tests_line)
        total_match = re.search(r'(\d+)\s+total', tests_line)

        if failed_match:
            failed_count = int(failed_match.group(1))
        if passed_match:
            passed_count = int(passed_match.group(1))
        if total_match:
            total_count = int(total_match.group(1))

    return {
        'suite_failed': suited_failed_count,
        'passed': passed_count,
        'failed': failed_count,
        'total': total_count
    }

if __name__ == "__main__":
#     Test 1: Working function
    py_function_code = """
def run_code(nums, target):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []
"""
    
    input = {"nums": [2, 7, 11, 15], "target": 9}
    output, error = execute_python(py_function_code, input)
    print(f"Output: {output}")
    print(f"Error: {error}")
    
    # Test 2: Function with error
    broken_function_code = """
def run_code(nums, target):
    return nums[100]  # Index error
"""

    output2, error2 = execute_python(broken_function_code, input)
    print(f"Output: {output2}")
    print(f"Error: {error2}")

    # Test 3: Jest Function 
    js_test_code = """
describe('basic test', () => {
    test('adds 1 + 2 to equal 3', () => {
        expect(1 + 2).toBe(3);
    });
});

describe('basic test', () => {
    test('adds 1 + 1 to equal 3', () => {
        expect(1 + 1).toBe(3);
    });
});

"""
    failures = asyncio.run(execute_jest_test(js_test_code))
    print(failures)
    if isinstance(failures, list):
        for failure in failures:
            print(f"❌ Failed: {failure['suite']} › {failure['test']}")
            print(f"   Expected: {failure['expected']}")
            print(f"   Received: {failure['received']}")
    else: 
        print("no error")
