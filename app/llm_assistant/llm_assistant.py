import os.path

import ollama


class AssistantLLM:
    """
    A Class to process the incoming chats and use tools to expand functionality
    """

    def __init__(self, ollama_model_name: str, tools_class=None, runtime_params=None):
        self.ollama_model_name = ollama_model_name
        self.tools_class = tools_class
        self.runtime_params = runtime_params
        self.chat_messages = [{'role': 'system', 'content': self._extract_sys_prompt_txt()}]

    # Public Methods (Main Functionality)
    def process_casual_user_prompt(self, prompt: str):
        self._add_prompt_to_messages(role='user', prompt=prompt)
        llm_response = self._respond_messages(add_tools=False)
        self._add_prompt_to_messages(role=llm_response.message.role, prompt=llm_response.message.content)
        return llm_response

    # Private Methods (Class methods)
    def _add_prompt_to_messages(self, role: str, prompt: str):
        if not self._is_valid_role(role):
            raise ValueError("Invalid role. Must be 'system', 'user', 'tool' or 'assistant'.")
        # Check if the type of message is a user or assistant prompt
        elif role and prompt:
            self.chat_messages.append({'role': role,
                                       'content': prompt})
        else:
            raise ValueError("Invalid arguments. Cannot add prompt to messages.")

    def _respond_messages(self, add_tools: bool = None):
        return ollama.chat(
            self.ollama_model_name,
            messages=self.chat_messages,
            options=self.runtime_params
        )

    @staticmethod
    def _is_valid_role(role: str) -> bool:
        return role in {"system", "user", "assistant", "tool"}

    @staticmethod
    def _extract_sys_prompt_txt() -> str:
        """
        Reads the txt file containing the System Prompt
        """
        file_name = '../system_prompts/sys_prompt.txt'
        file_path = os.path.join(os.path.dirname(__file__), file_name)
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
            return text
        except Exception as e:
            print(f"Error reading llm system prompt file: {e}")
            return ""
