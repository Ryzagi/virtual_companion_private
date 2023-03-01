from langchain import PromptTemplate


class ConversationPrompt:
    memory_key = "chat_history"
    user_input_key = "user_input"
    conversation_tone_key = "conversation_tone"

    def __init__(
        self,
        prompt_text: str,
        user_name: str = "Man",
        chatbot_name: str = "You",
    ):
        string_base_template = """PROMPT_TEXT
{chat_history}
USER_NAME: {user_input}
CHATBOT_NAME ({conversation_tone}):"""
        string_base_template = string_base_template.replace(
            "PROMPT_TEXT", prompt_text
        )
        string_base_template = string_base_template.replace(
            "USER_NAME", user_name
        )
        string_base_template = string_base_template.replace(
            "CHATBOT_NAME", chatbot_name
        )
        #print(string_base_template)
        self._prompt = PromptTemplate(
            input_variables=["chat_history", "user_input", "conversation_tone"],
            template=string_base_template,
        )

        self._user_name = user_name
        self._chatbot_name = chatbot_name

    @property
    def prompt(self) -> PromptTemplate:
        return self._prompt

    @property
    def chatbot_name(self) -> str:
        return self._chatbot_name

    @property
    def user_name(self) -> str:
        return self._user_name


class RomanticConversationPrompt(ConversationPrompt):
    """
    Prompt for romantic conversation between a human and a chatbot.

    Args:
        prompt_template: The template for the prompt.
        name: The name of the chatbot.
        age: The age of the chatbot.
        interests: The interests of the chatbot.
        profession: The profession of the chatbot.
        gender: The gender of chatbot.
    """

    def __init__(
        self,
        prompt_template: str,
        name: str = "Alisa",
        age: str = "25",
        interests: str = "Nothing",
        profession: str = "Singer",
        gender: str = "Female",
    ):
        prompt_template = prompt_template.format(
            name=name,
            age=age,
            interests=interests,
            profession=profession,
            gender=gender,
        )
        super(RomanticConversationPrompt, self).__init__(
            prompt_text=prompt_template,
            user_name="Human",
            chatbot_name=name,
        )
