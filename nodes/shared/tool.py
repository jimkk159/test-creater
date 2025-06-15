from .base import BaseSharedManager
from ..constants import SharedKeys

class ToolSharedManager(BaseSharedManager):
    @staticmethod
    def init_file_section(shared):
        """Initialize the file section in shared state"""
        if SharedKeys.FILE not in shared:
            shared[SharedKeys.FILE] = {}

    @staticmethod
    def store_tools(shared, tools):
        """Store tools in shared state"""
        ToolSharedManager.init_file_section(shared)
        BaseSharedManager.store_list(shared, [SharedKeys.FILE, SharedKeys.TOOLS], tools)

    @staticmethod
    def store_tool_info(shared, tool_info):
        """Store formatted tool information"""
        ToolSharedManager.init_file_section(shared)
        BaseSharedManager.store_value(shared, [SharedKeys.FILE, SharedKeys.TOOL_INFO], tool_info)

    @staticmethod
    def store_decision_response(shared, response):
        """Store the decision response data"""
        ToolSharedManager.init_file_section(shared)
        BaseSharedManager.store_value(shared, [SharedKeys.FILE, SharedKeys.ACTION], response.get('action', ""))
        BaseSharedManager.store_value(shared, [SharedKeys.FILE, SharedKeys.TOOL_NAME], response.get("tool", ""))
        BaseSharedManager.store_value(shared, [SharedKeys.FILE, SharedKeys.PARAMETERS], response.get("parameters", ""))
        BaseSharedManager.store_value(shared, [SharedKeys.FILE, SharedKeys.THINKING], response.get("thinking", ""))

    @staticmethod
    def store_tool_result(shared, result):
        """Store tool execution result"""
        ToolSharedManager.init_file_section(shared)
        BaseSharedManager.store_value(shared, [SharedKeys.FILE, SharedKeys.TOOL_RESULT], result)

    @staticmethod
    def get_action(shared):
        """Get the current action from shared state"""
        return BaseSharedManager.get_value(shared, [SharedKeys.FILE, SharedKeys.ACTION], "")

    @staticmethod
    def get_tool_name(shared):
        """Get the current tool name from shared state"""
        return BaseSharedManager.get_value(shared, [SharedKeys.FILE, SharedKeys.TOOL_NAME], "")

    @staticmethod
    def get_parameters(shared):
        """Get the current parameters from shared state"""
        return BaseSharedManager.get_value(shared, [SharedKeys.FILE, SharedKeys.PARAMETERS], "")

    @staticmethod
    def get_tool_result(shared):
        """Get the current tool result from shared state"""
        return BaseSharedManager.get_value(shared, [SharedKeys.FILE, SharedKeys.TOOL_RESULT], "")
    
    @staticmethod
    def get_file_structure(shared):
        """Get the file structure from shared state"""
        return BaseSharedManager.get_value(shared, [SharedKeys.FILE, SharedKeys.FILE_STRUCTURE], {}) 

    @staticmethod
    def set_final_result(shared, result):
        """Set the final result"""
        ToolSharedManager.init_file_section(shared)
        BaseSharedManager.store_value(shared, [SharedKeys.FILE, SharedKeys.RESULT], result)

    @staticmethod
    def store_file_structure(shared, structure):
        """Store the file structure from directory tree tool"""
        ToolSharedManager.init_file_section(shared)
        BaseSharedManager.store_value(shared, [SharedKeys.FILE, SharedKeys.FILE_STRUCTURE], structure)
