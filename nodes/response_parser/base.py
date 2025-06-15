import yaml
from typing import Dict, Any

class ResponseParser:
    @staticmethod
    def parse_yaml_response(response: str) -> Dict[str, Any]:
        """Parse YAML response from LLM and extract the YAML content"""
        try:
            yaml_str = response.split("```yaml")[1].split("```")[0].strip()
            return yaml.safe_load(yaml_str)
        except (IndexError, yaml.YAMLError) as e:
            raise ValueError(f"Failed to parse YAML response: {e}")

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