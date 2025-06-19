import os
from myPocketFlow import AsyncFlow, AsyncParallelBatchFlow
from nodes import ReturnDefaultActionNode, CopyFileNode
from nodes import GetToolsNode, DecideToolNode, ExecuteToolNode
from nodes import (
    GenerateTestCasesNode,
    RunTestsNode,
    ImplementFunctionNode,
    AnalyzeNode,
    ReviseNode,
    FileCoordinatorNode,
)

from utils.utils import save_to_file
from config import SharedKeys, SystemConfig


def save_to_file_iteration(shared):
    test_codes_to_file = ""
    if SharedKeys.TEST_CODE not in shared:
        shared[SharedKeys.TEST_CODE] = []
    for i, func_name in enumerate(shared[SharedKeys.TEST_CODE]):
        test_codes_to_file += f"{shared[SharedKeys.TEST_CODE][func_name]}\n\n"
    save_to_file(test_codes_to_file, "final.test.js")


def Read_and_find_file_flow():
    """Find the file and then read its content"""
    # Create nodes
    get_tools_node = GetToolsNode()
    decide_node = DecideToolNode()
    execute_node = ExecuteToolNode()

    # Error handling
    decide_node - "error" >> decide_node

    # Create the final node to return "default"
    return_default_node = ReturnDefaultActionNode()

    # Connect nodes
    get_tools_node >> decide_node
    decide_node - "tool" >> execute_node
    execute_node - "tool_result" >> decide_node

    # If decide_node returns anything other than "tool" (like default), go to return_default_node

    decide_node >> return_default_node
    # This connects the default action of decide_node

    # Create flow starting with test generation
    return AsyncFlow(start=get_tools_node)


def Implement_flow():
    implement_function = ImplementFunctionNode(max_retries=1, wait=0)
    return AsyncFlow(start=implement_function)


# --- Flow Creation ---
def Run_test_flow():
    """Creates and returns the parallel translation flow."""
    copy_file_node = CopyFileNode(
        dir_path=os.path.join(os.getcwd(), SystemConfig.TEST_DIRECTORY),
        suffix="_suggestion",
        is_use_function_name=True,
    )
    generate_test_cases = GenerateTestCasesNode(max_retries=1, wait=0)
    implement_flow = Implement_flow()

    run_tests = RunTestsNode()
    revise = ReviseNode(max_retries=1, wait=2)
    return_default_node = ReturnDefaultActionNode()

    # Error handling
    copy_file_node >> generate_test_cases
    generate_test_cases - "error" >> generate_test_cases
    implement_flow - "error" >> implement_flow
    revise - "error" >> revise

    generate_test_cases >> implement_flow
    implement_flow >> run_tests
    run_tests - "failure" >> revise
    run_tests >> return_default_node
    revise >> run_tests

    return AsyncFlow(start=copy_file_node)


class FunctionParallelBatchFlow(AsyncParallelBatchFlow):
    async def prep_async(self, shared):
        # Get all functions from shared store
        functions = shared.get(SharedKeys.FUNCTIONS, {})
        # Create a list of params for each function
        return [
            {SharedKeys.FUNCTION_NAME: name, SharedKeys.FUNCTION_CONTENT: content}
            for name, content in functions.items()
        ]

    async def post_async(self, shared, prep_res, exec_res):
        # Save the test code to a file
        print("🎉All tests passed across all batches!")


def auto_code_test_generate_flow():
    """Automatically Generate test code and execute the code to ensure the code quality"""

    # Create flows or nodes
    read_and_find_file_flow = Read_and_find_file_flow()
    analyze_node = AnalyzeNode()

    run_test_flow = Run_test_flow()

    # Create a batch flow for running tests on each function
    function_parallel_batch = FunctionParallelBatchFlow(start=run_test_flow)

    # Combine test code and suggested file
    file_coordinator = FileCoordinatorNode()

    # Connect nodes
    read_and_find_file_flow >> analyze_node
    analyze_node >> function_parallel_batch
    # function_parallel_batch >> file_coordinator

    # Create flow starting with test generation
    return AsyncFlow(start=read_and_find_file_flow)
