"""
LLM Client Module - Handles all ChatGPT/LLM interactions.
This module can be easily replaced with another LLM provider in the future.
"""

from typing import Optional, List, Dict, Iterator
from openai import OpenAI


class LLMClient:
    def __init__(self, config: Optional[dict] = None):
        self.api_key = None
        self.model = None
        self.max_output_tokens = None

        if config:
            self.api_key = config.get("api_key")
            self.model = config.get("model")
            # Keep backward compatibility with existing config key.
            self.max_output_tokens = config.get(
                "max_output_tokens", config.get("max_completion_tokens")
            )
        self.conversation_history: List[Dict[str, str]] = []

        # Initialize the OpenAI client
        self.client = OpenAI(api_key=self.api_key)

    def send_message(
        self,
        message: str,
        system_prompt: Optional[str] = None,
        reset_history: bool = False,
    ) -> Iterator[str]:
        """
        Send a message and stream the response.
        
        Yields chunks of the response as they arrive.
        """
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

        # print("MESSAGES:", messages)
        try:
            assistant_message = ""

            # Stream the response using the Responses API.
            with self.client.responses.stream(
                model=self.model,
                input=messages,
                max_output_tokens=self.max_output_tokens,
            ) as stream:
                for event in stream:
                    if event.type == "response.output_text.delta" and event.delta:
                        assistant_message += event.delta
                        yield event.delta

            # Update conversation history after streaming is complete
            self.conversation_history.append({"role": "user", "content": message})
            self.conversation_history.append(
                {"role": "assistant", "content": assistant_message}
            )

        except Exception as e:
            raise Exception(f"Error communicating with LLM: {str(e)}")

    def reset_conversation(self):
        self.conversation_history = []
