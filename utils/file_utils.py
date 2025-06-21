import os
from config import SystemConfig

def create_copy_file_path(original_file_path: str) -> str:
    """
    Create a copy file path by adding '_copy' suffix to the original filename.
    
    Args:
        original_file_path: Path to the original file
        
    Returns:
        Full path to the copy file in the test directory
    """
    original_filename = os.path.basename(original_file_path)
    filename_without_ext = os.path.splitext(original_filename)[0]
    file_extension = os.path.splitext(original_filename)[1]
    
    copy_filename = f"{filename_without_ext}_copy{file_extension}"
    return os.path.join(SystemConfig.TEST_DIRECTORY, copy_filename)