"""
LLM Client Module - Handles all ChatGPT/LLM interactions.
This module can be easily replaced with another LLM provider in the future.
"""

from typing import Optional, List, Dict
from openai import OpenAI

class LLMClient:
    def __init__(self, config: Optional[dict] = None):
        if config:
            self.api_key = config.get("api_key")
            self.model = config.get("model")
            self.max_tokens = config.get("max_tokens")
            self.temperature = config.get("temperature")
        self.conversation_history: List[Dict[str, str]] = []
        
        # Initialize the OpenAI client
        self.client = OpenAI(api_key=self.api_key)

    def send_message(self, message: str, system_prompt: Optional[str] = None,
                     reset_history: bool = False) -> str:
        if reset_history:
            self.conversation_history = []

        # Build messages list
        messages = []

        # Add system prompt if provided
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        # Add conversation history
        messages.extend(self.conversation_history)

        # Add current message
        messages.append({"role": "user", "content": message})

        #print("MESSAGES:", messages)
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )

            assistant_message = response.choices[0].message.content.strip()

            # Update conversation history
            self.conversation_history.append({"role": "user", "content": message})
            self.conversation_history.append({"role": "assistant", "content": assistant_message})

            return assistant_message

        except Exception as e:
            raise Exception(f"Error communicating with LLM: {str(e)}")

    def reset_conversation(self):
        self.conversation_history = []
