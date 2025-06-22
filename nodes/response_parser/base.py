import yaml
from typing import Dict, Any
import logging
from config import SystemConfig

# Set up logger
logger = logging.getLogger(__name__)

class ResponseParser:
    @staticmethod
    def parse_yaml_response(response: str) -> Dict[str, Any]:
        """Parse YAML response from LLM and extract the YAML content"""
        logger.debug("=== FULL LLM RESPONSE ===")
        logger.debug(response)
        logger.debug("=== END RESPONSE ===")
        new_yaml_str = ""
        try:
            yaml_str = response.split("```yaml")[1].split("```")[0].strip()
            logger.debug("=== EXTRACTED YAML ===")
            logger.debug(f"YAML string: {repr(yaml_str)}")
            logger.debug("=== END YAML ===")

            # Fix common YAML issues by quoting unquoted strings with colons
            output = {}
            try:
                output =yaml.safe_load(yaml_str)
                return output
            except Exception as e:
                logger.error("=== YAML PARSING ERROR ===")
                # Try to identify the problematic line
                lines = yaml_str.split('\n')
                for i, line in enumerate(lines):
                    print(line)
                logger.error("=== END ERROR ===")
                new_yaml_str = ResponseParser._fix_yaml_strings(yaml_str)
                output = yaml.safe_load(new_yaml_str)
            return output
        except (IndexError, yaml.YAMLError) as e:
            logger.error("=== YAML PARSING ERROR ===")
            print(SystemConfig.BORDER)
            # Try to identify the problematic line
            lines = new_yaml_str.split('\n')
            for i, line in enumerate(lines):
                print(line)
            logger.error("=== END ERROR ===")
            raise ValueError(f"Failed to parse YAML response: {e}")
    
    @staticmethod
    def _fix_yaml_strings(yaml_str: str) -> str:
        """Fix common YAML string and indentation issues"""
        import re
        lines = yaml_str.split('\n')
        fixed_lines = []
        
        for i, line in enumerate(lines):
            # If this line is part of a list item, fix the indentation
            if i > 0 and '- ' in lines[i-1]:  # Previous line had a list marker
                # Find the indentation of the list marker line
                prev_line = lines[i-1]
                list_marker_pos = prev_line.find('- ')
                if list_marker_pos >= 0:
                    # All properties should align with the property after `-`
                    target_indent = list_marker_pos + 2  # 2 spaces after `-`
                    content = line.lstrip()
                    if content:  # Don't fix empty lines
                        line = ' ' * target_indent + content
            
            fixed_lines.append(line)
        
        return '\n'.join(fixed_lines)

    @staticmethod
    def validate_decision_response(parsed_response: Dict[str, Any]) -> None:
        """Validate that the decision response has required fields"""
        required_fields = ["action"]
        for field in required_fields:
            if field not in parsed_response:
                raise ValueError(f"Missing required field: {field}")
        
        valid_actions = ["tool", "done", "error"]
        action = parsed_response["action"]
        if action not in valid_actions:
            raise ValueError(f"Invalid action '{action}'. Must be one of: {valid_actions}")
        
        # If action is tool, validate tool-specific fields
        if action == "tool":
            if "tool" not in parsed_response:
                raise ValueError("Tool action requires 'tool' field")
            if "parameters" not in parsed_response:
                raise ValueError("Tool action requires 'parameters' field") 
            
    @staticmethod
    def validate_supervise_response(parsed_response: Dict[str, Any]) -> None:
        """Validate that the decision response has required fields"""
        required_fields = ["action"]
        for field in required_fields:
            if field not in parsed_response:
                raise ValueError(f"Missing required field: {field}")
        
        valid_actions = ["suggest", "done", "error"]
        action = parsed_response["action"]
        if action not in valid_actions:
            raise ValueError(f"Invalid action '{action}'. Must be one of: {valid_actions}")
        
        # If action is tool, validate tool-specific fields
        if action == "suggest":
            if "suggestion" not in parsed_response:
                raise ValueError("Suggest action requires 'suggestion' field")