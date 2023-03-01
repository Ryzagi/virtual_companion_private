import time
from csv import QUOTE_MINIMAL, writer
from pathlib import Path
from typing import Dict

from converbot.constants import CONVERSATION_SAVE_DIR, HISTORY_SAVE_DIR
from converbot.core import GPT3Conversation


class ConversationDB:
    """
    A database for storing conversations with GPT-3 chatbots.

    Args:
        chat_history_save_dir: The directory to save chat history to.
        conversation_save_dir: The directory to save conversations to.
    """

    def __init__(
        self,
        chat_history_save_dir: Path = HISTORY_SAVE_DIR,
        conversation_save_dir: Path = CONVERSATION_SAVE_DIR,
    ) -> None:
        self._conversation_save_dir = conversation_save_dir
        self._chat_history_save_dir = chat_history_save_dir
        self._conversation_save_dir.mkdir(parents=True, exist_ok=True)
        self._chat_history_save_dir.mkdir(parents=True, exist_ok=True)

        self._user_to_conversation: Dict[str, GPT3Conversation] = {}

    def exists(self, user_id: int) -> bool:
        return str(user_id) in self._user_to_conversation

    def remove_conversation(self, user_id: int) -> None:
        self._user_to_conversation.pop(str(user_id), None)

    def get_conversation(self, user_id: int) -> GPT3Conversation:
        return self._user_to_conversation.get(str(user_id), None)

    def add_conversation(
        self, user_id: int, conversation: GPT3Conversation
    ) -> None:
        self._user_to_conversation[str(user_id)] = conversation

    def write_chat_history(
        self, user_id: int, message: str, chatbot_response: str
    ) -> None:
        """
        Write the chat history to disk.

        Args:
            user_id: The user ID.
            message: The user's message.
            chatbot_response: The chatbot's response.

        Returns: None
        """
        user_id = str(user_id)
        filename = self._chat_history_save_dir / f"{user_id}.csv"
        is_already_exist = filename.exists()

        with (self._chat_history_save_dir / f"{user_id}.csv").open("a", encoding="utf-8") as f:
            csv_writer = writer(
                f, delimiter=",", quotechar='"', quoting=QUOTE_MINIMAL
            )
            if not is_already_exist:
                csv_writer.writerow(
                    ["time", "user_message", "chatbot_response"]
                )

            csv_writer.writerow([time.time(), message, chatbot_response])

    def serialize_conversations(self) -> None:
        """
        Serialize the conversations to disk.

        Returns: None
        """
        for user_id, conversation in self._user_to_conversation.items():
            conversation.serialize(user_id, self._conversation_save_dir)

    def __del__(self) -> None:
        """
        Serialize the conversations to disk when the object is deleted.
        """
        self.serialize_conversations()
