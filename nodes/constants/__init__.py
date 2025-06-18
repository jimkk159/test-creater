"""
DEPRECATED: This constants module has been moved to config/ directory.
This file is kept for backward compatibility.
"""

import warnings

# Issue deprecation warning
warnings.warn(
    "nodes/constants is deprecated. Use 'from config import SharedKeys, Actions, etc.' instead.",
    DeprecationWarning,
    stacklevel=2
)

# Import from new location for backward compatibility
from config import SharedKeys, Actions, TestActions, ToolActions, SystemConfig

# Import from old files for any remaining backward compatibility
from .base import *
from .test import *
from .tool import *

__all__ = [
    # Base constants
    'BORDER_LEN', 'SYSTEM_MAX_LOOP', 'BORDER', 'MCP_SERVER_PATH',
    'Actions', 'SharedKeys',
    
    # Test constants
    'MAX_ITERATION', 'TestActions', 'TestStatus',
    
    # Tool constants
    'ToolActions', 'ToolKeys'
] 