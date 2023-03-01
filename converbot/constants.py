from pathlib import Path
from converbot.utils import read_json_file
CONVERSATION_SAVE_DIR = (
    Path(__file__).parent.parent / "database" / "saved_conversations"
)
HISTORY_SAVE_DIR = Path(__file__).parent.parent / "database" / "chat_history"

TIME, USER_MESSAGE, CHATBOT_RESPONSE = (
    "time",
    "user_message",
    "chatbot_response",
)

DEFAULT_CONFIG_PATH = Path(__file__).parent.parent / "config" / "config.json"
DEFAULT_FRIENDLY_TONE = read_json_file(DEFAULT_CONFIG_PATH)["mood"]