import json
from dataclasses import dataclass
from pathlib import Path



@dataclass
class RomanitcConversationConfig:
    """
    The configuration for the romantic conversation.

    Args:
        prompt_template: The template for the prompt.
        summary_buffer_memory_max_token_limit: The maximum number of tokens in the summary buffer.
    """

    prompt_template: str
    model: str
    mood: str
    temperature: float
    max_tokens: int
    top_p: float
    frequency_penalty: float
    presence_penalty: float
    best_of: int
    summary_buffer_memory_max_token_limit: int = 1000
    def to_json(self, save_path: Path) -> None:
        """
        Save the configuration to a json file.

        Args:
            save_path: The path to save the configuration.
        """
        with open(save_path, "w") as f:
            json.dump(self.__dict__, f, indent=4)

    @classmethod
    def from_json(cls, load_path: Path) -> "RomanitcConversationConfig":
        """
        Load the configuration from a json file.

        Args:
            load_path: The path to load the configuration.

        Returns:
            The configuration.
        """

        return cls(**json.loads(load_path.read_text()))