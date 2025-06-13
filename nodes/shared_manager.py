from .constants import SharedKeys, Actions

class SharedManager:
    @staticmethod
    def init_file_section(shared):
        """Initialize the file section in shared state if it doesn't exist"""
        if SharedKeys.FILE not in shared:
            shared[SharedKeys.FILE] = {}

    @staticmethod
    def store_tools(shared, tools):
        """Store tools in shared state"""
        SharedManager.init_file_section(shared)
        if SharedKeys.TOOLS not in shared[SharedKeys.FILE]:
            shared[SharedKeys.FILE][SharedKeys.TOOLS] = []
        shared[SharedKeys.FILE][SharedKeys.TOOLS].append(tools)

    @staticmethod
    def store_tool_info(shared, tool_info):
        """Store formatted tool information"""
        SharedManager.init_file_section(shared)
        shared[SharedKeys.FILE][SharedKeys.TOOL_INFO] = tool_info

    @staticmethod
    def store_decision_response(shared, response):
        """Store the decision response data"""
        SharedManager.init_file_section(shared)
        shared[SharedKeys.FILE][SharedKeys.ACTION] = response.get('action', "")
        shared[SharedKeys.FILE][SharedKeys.TOOL_NAME] = response.get("tool", "")
        shared[SharedKeys.FILE][SharedKeys.PARAMETERS] = response.get("parameters", "")
        shared[SharedKeys.FILE][SharedKeys.THINKING] = response.get("thinking", "")

    @staticmethod
    def store_tool_result(shared, result):
        """Store tool execution result"""
        SharedManager.init_file_section(shared)
        shared[SharedKeys.FILE][SharedKeys.TOOL_RESULT] = result

    @staticmethod
    def get_action(shared):
        """Get the current action from shared state"""
        return shared.get(SharedKeys.FILE, {}).get(SharedKeys.ACTION, "")

    @staticmethod
    def get_tool_name(shared):
        """Get the current tool name from shared state"""
        return shared.get(SharedKeys.FILE, {}).get(SharedKeys.TOOL_NAME, "")

    @staticmethod
    def get_parameters(shared):
        """Get the current parameters from shared state"""
        return shared.get(SharedKeys.FILE, {}).get(SharedKeys.PARAMETERS, "")

    @staticmethod
    def get_tool_result(shared):
        """Get the current tool result from shared state"""
        return shared.get(SharedKeys.FILE, {}).get(SharedKeys.TOOL_RESULT, "")

    @staticmethod
    def set_final_result(shared, result):
        """Set the final result"""
        SharedManager.init_file_section(shared)
        shared[SharedKeys.FILE][SharedKeys.RESULT] = result 