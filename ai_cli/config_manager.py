import json
from pathlib import Path
from typing import Optional
from pathlib import Path
import json, importlib.resources as resources
from collections.abc import Mapping


class ConfigManager:
    def __init__(self):
        self.history_file = Path.home() / ".ai_history"
        self.config = self.load_config()

    def load_config(self) -> dict:
        with resources.files("ai_cli.data").joinpath("default_config.json").open("r") as f:
            config = json.load(f)

        # Check for user overrides
        user_config = Path.home() / ".ai_cli_config.json"
        if user_config.exists():
            with open(user_config) as f:
                user_overrides = json.load(f)
                deep_update(config, user_overrides)

        # Validate config structure
        if "prompts" not in config:
            raise ValueError("Missing 'prompts' key in config")
        
        if not isinstance(config["prompts"], list):
            raise ValueError("'prompts' must be a list")
        
        # Ensure at least default prompt exists
        if not any(p.get("name") == "default" for p in config["prompts"]):
            config["prompts"].insert(0, {"name": "default", "prompt": ""})
        return config

    def get_prompt_by_name(self, name: str) -> Optional[str]:
        for prompt_item in self.config["prompts"]:
            if prompt_item.get("name") == name:
                return prompt_item.get("prompt", "")
        return None

    def get_openai_config(self) -> str:
        config = self.config.get("openai")
        if not config:
            raise ValueError(
                "OpenAI configuration not found. Please set the openai configuration in the configuration."
            )
        return config
    
    def get_history_file(self) -> Path:
        return self.history_file

def deep_update(original, updates):
    """
    Recursively update a dictionary with another dictionary.
    Merges nested dicts instead of overwriting them.
    """
    for key, value in updates.items():
        if isinstance(value, Mapping) and isinstance(original.get(key), Mapping):
            deep_update(original[key], value)
        else:
            original[key] = value
    return
