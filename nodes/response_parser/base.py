import yaml
from typing import Dict, Any
import logging

# Set up logger
logger = logging.getLogger(__name__)

class ResponseParser:
    @staticmethod
    def parse_yaml_response(response: str) -> Dict[str, Any]:
        """Parse YAML response from LLM and extract the YAML content"""
        logger.debug("=== FULL LLM RESPONSE ===")
        logger.debug(response)
        logger.debug("=== END RESPONSE ===")
        
        try:
            yaml_str = response.split("```yaml")[1].split("```")[0].strip()
            
            logger.debug("=== EXTRACTED YAML ===")
            logger.debug(f"YAML string: {repr(yaml_str)}")
            logger.debug("=== END YAML ===")
            
            # Fix common YAML issues by quoting unquoted strings with colons
            yaml_str = ResponseParser._fix_yaml_strings(yaml_str)
            
            return yaml.safe_load(yaml_str)
        except (IndexError, yaml.YAMLError) as e:
            logger.error("=== YAML PARSING ERROR ===")
            logger.error(f"Error: {e}")
            logger.error(f"YAML content that failed: {repr(yaml_str) if 'yaml_str' in locals() else 'No YAML extracted'}")
            logger.error("=== END ERROR ===")
            raise ValueError(f"Failed to parse YAML response: {e}")
    
    @staticmethod
    def _fix_yaml_strings(yaml_str: str) -> str:
        """Fix common YAML string and indentation issues"""
        import re
        lines = yaml_str.split('\n')
        fixed_lines = []
        in_literal_block = False
        literal_indent_level = 0
        
        for i, line in enumerate(lines):
            # Fix indentation: convert 8-space indents to 4-space
            if line.startswith('        '):  # 8 spaces
                line = '    ' + line[8:]  # Convert to 4 spaces
            
            # Check if we're starting a literal block (line ending with |)
            if line.strip().endswith('|'):
                in_literal_block = True
                # Calculate the base indentation level for this block
                literal_indent_level = len(line) - len(line.lstrip()) + 4  # Add 4 for literal block content
                fixed_lines.append(line)
                continue
            
            # If we're in a literal block, ensure proper indentation
            if in_literal_block:
                if line.strip() == '':  # Empty line
                    fixed_lines.append(line)
                    continue
                elif line.startswith('    - ') or line.startswith('- '):  # New list item, exit literal block
                    in_literal_block = False
                    literal_indent_level = 0
                else:
                    # Ensure the line has the proper indentation for literal block content
                    content = line.lstrip()
                    if content:  # Non-empty line
                        line = ' ' * literal_indent_level + content
            
            # Match lines like "expected: Error: Division by zero"
            match = re.match(r'^(\s*expected:\s*)(.*)$', line)
            if match:
                indent_and_key = match.group(1)
                value = match.group(2).strip()
                
                # If value contains colon and isn't already quoted, quote it
                if ':' in value and not (value.startswith('"') and value.endswith('"')) and not (value.startswith("'") and value.endswith("'")):
                    line = f'{indent_and_key}"{value}"'
            
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