from pathlib import Path
import json
from langchain import LLMChain
from langchain.callbacks.base import CallbackManager
from langchain.chains import load_chain
from langchain.chains.conversation.memory import ConversationSummaryBufferMemory
from langchain.llms import OpenAI

from converbot.utils import read_json_file
from converbot.constants import CONVERSATION_SAVE_DIR, DEFAULT_FRIENDLY_TONE, DEFAULT_CONFIG_PATH
from converbot.mood_handler import ConversationToneHandler
from converbot.prompt import ConversationPrompt
from converbot.callbacks import DebugPromptCallback


class GPT3Conversation:
    """
    A conversation with a GPT-3 chatbot.

    Args:
        prompt: The prompt for the conversation.
        verbose: Whether to print verbose output.
        summary_buffer_memory_max_token_limit: The maximum number of tokens to store in the summary buffer memory.
    """

    def __init__(
        self,
        prompt: ConversationPrompt,
        tone: str = DEFAULT_FRIENDLY_TONE,
        verbose: bool = False,
        summary_buffer_memory_max_token_limit: int = 500,
    ):
        self._prompt = prompt
        config = read_json_file(DEFAULT_CONFIG_PATH)
        self._language_model = OpenAI(model_name=config["model"],
                                      temperature=config["temperature"],
                                      max_tokens=config["max_tokens"],
                                      top_p=config["top_p"],
                                      frequency_penalty=config["frequency_penalty"],
                                      presence_penalty=config["presence_penalty"],
                                      best_of=config["best_of"]
                                      )
        self._memory = ConversationSummaryBufferMemory(
            llm=self._language_model,
            max_token_limit=summary_buffer_memory_max_token_limit,
            input_key=self._prompt.user_input_key,
            memory_key=self._prompt.memory_key,
            human_prefix=self._prompt.user_name,
            ai_prefix=self._prompt.chatbot_name,
        )
        self._debug_callback = DebugPromptCallback()
        self._conversation = LLMChain(
            llm=self._language_model,
            memory=self._memory,
            prompt=self._prompt.prompt,
            verbose=verbose,
            callback_manager=CallbackManager([self._debug_callback])
        )

        self._tone_processor = ConversationToneHandler()
        self._tone = self._tone_processor(tone)
        self._debug = False

    def change_debug_mode(self):
        self._debug = not self._debug
        return self._debug

    def set_tone(self, tone: str) -> None:
        """
        Set the tone of the chatbot.

        Args:
            tone: The tone of the chatbot.

        Returns: None
        """
        self._tone = self._tone_processor(tone)

    def ask(self, user_input: str) -> str:
        """
        Ask the chatbot a question and get a response.

        Args:
            user_input: The question to ask the chatbot.

        Returns: The response from the chatbot.
        """
        output = self._conversation.predict(
            **{
                self._prompt.user_input_key: user_input,
                self._prompt.conversation_tone_key: self._tone,
                self._prompt.memory_key: self._memory,
            },
        )

        if not self._debug:
            return output

        return self._debug_callback.last_used_prompt + output

    def serialize(
        self, chatbot_name: str, serialize_dir: Path = CONVERSATION_SAVE_DIR
    ) -> None:
        """
        Serialize the chatbot to disk.

        Args:
            serialize_dir: The directory to serialize the chatbot to.
            chatbot_name: The name of the chatbot.
        """
        serialize_dir.mkdir(exist_ok=True)
        self._conversation.save(
            (serialize_dir / chatbot_name).with_suffix(".json")
        )

    def load(
        self, chatbot_name: str, serialize_dir: Path = CONVERSATION_SAVE_DIR
    ) -> None:
        """
        Load a chatbot from disk.

        Args:
            serialize_dir: The directory to load the chatbot from.
            chatbot_name: The name of the chatbot.
        """
        self._conversation = load_chain(
            (serialize_dir / chatbot_name).with_suffix(".json")
        )


