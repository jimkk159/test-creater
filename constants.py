"""
Legacy constants file. 
New constants are now organized in the config/ directory.
This file is kept for backward compatibility.
"""

# Import all new constants for backward compatibility
from config import SharedKeys, Actions, TestActions, ToolActions, SystemConfig

# Legacy constants that still work
TEST_DIRECTORY = SystemConfig.TEST_DIRECTORY

# Re-export everything for backward compatibility
__all__ = [
    'SharedKeys', 'Actions', 'TestActions', 'ToolActions', 'SystemConfig',
    'TEST_DIRECTORY'
]