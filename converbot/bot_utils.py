import json
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

from converbot.config import RomanitcConversationConfig
from converbot.context_handler import ConversationBotContextHandler
from converbot.core import GPT3Conversation
from converbot.prompt import RomanticConversationPrompt, ConversationPrompt
from converbot.txtstyle_handler import ConversationTextStyleHandler


@dataclass
class ConversationContext:
    name: str
    age: str
    interests: str
    profession: str
    gender: str


def parse_context(message: str) -> Optional[ConversationContext]:
    """
    Parse context string and return it as ConversationContext object.

    Args:
        message: The context string.


    Returns:
        The ConversationContext object.
    """
    splitted_message = message.split(",")
    if len(splitted_message) != 5:
        return None
    else:
        name, age, interests, profession, gender = message.split(",")
        return ConversationContext(
            name=name,
            age=age,
            interests=interests,
            profession=profession,
            gender=gender,
        )


def create_conversation_from_context(
        context: str,
        tone: str,
        config_path: Path,
) -> GPT3Conversation:
    """
    Create a conversation from the context.

    Args:
        context: The context.

    Returns: The conversation.
    """
    config = RomanitcConversationConfig.from_json(config_path)
    text_style = ConversationTextStyleHandler()(context)
    context_summary = ConversationBotContextHandler()(context)

    conversation = GPT3Conversation(
        tone=tone,
        prompt=ConversationPrompt(
            prompt_text=config.prompt_template + '\nYou are an AI model pretending to be a human. You cannot make plans or meet anyone in the real world. You are unable to leave your computer.\n\nInformation about [Bot]:\n' + context_summary + '\n\nFollowing text defines [Bot] texting style and messaging style:' + text_style + '\n\nYou are an AI model pretending to be a human. You cannot make plans or meet anyone in the real world. You are unable to leave your computer.\n\nConversation:\n[Bot]: Lets start the conversation, can you tell me a little about yourself?',
            user_name="[User]",
            chatbot_name="[Bot]"
        ),
        summary_buffer_memory_max_token_limit=config.summary_buffer_memory_max_token_limit,
    )
    return conversation
