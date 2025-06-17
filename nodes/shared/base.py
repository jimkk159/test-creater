class BaseSharedManager:
    @staticmethod
    def init_section(shared, section_key):
        """Initialize a section in shared state if it doesn't exist"""
        if section_key not in shared:
            shared[section_key] = {}

    @staticmethod
    def store_value(shared, keys, value):
        """Store a value using hierarchical keys
        
        Args:
            shared: The shared state dictionary
            keys: List of keys representing the hierarchy path
            value: The value to store
        """
        current = shared
        
        # Navigate through all keys except the last one
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
            
        # Set the value at the final key
        current[keys[-1]] = value

    @staticmethod
    def get_value(shared, keys, default=None):
        """Get a value using hierarchical keys with default
        
        Args:
            shared: The shared state dictionary
            keys: List of keys representing the hierarchy path
            default: Default value if path doesn't exist
        """
        current = shared
        
        # Navigate through all keys
        for key in keys:
            if not isinstance(current, dict) or key not in current:
                return default
            current = current[key]
            
        return current

    @staticmethod
    def store_dict(shared, keys, value_dict):
        """Store a dictionary using hierarchical keys
        
        Args:
            shared: The shared state dictionary
            keys: List of keys representing the hierarchy path
            value_dict: Dictionary to store
        """
        current = shared
        
        # Navigate through all keys except the last one
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
            
        # Initialize or update the dictionary at the final key
        if keys[-1] not in current:
            current[keys[-1]] = {}
        current[keys[-1]].update(value_dict)

    @staticmethod
    def store_list(shared, keys, value):
        """Store a value in a list using hierarchical keys
        
        Args:
            shared: The shared state dictionary
            keys: List of keys representing the hierarchy path
            value: Value to append to the list
        """
        current = shared
        
        # Navigate through all keys except the last one
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
            
        # Initialize or append to the list at the final key
        if keys[-1] not in current:
            current[keys[-1]] = []
        current[keys[-1]].extend(value) 