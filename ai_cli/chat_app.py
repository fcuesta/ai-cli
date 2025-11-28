#!/usr/bin/env python3
"""
AI Chat Application - Command line ChatGPT client with interactive and non-interactive modes.
"""

import argparse
import os
import sys
from typing import Optional

from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory

from config_manager import ConfigManager
from llm_client import LLMClient
from prompt_processor import PromptProcessor


class ChatApp:
    def __init__(self):
        self.config_manager = ConfigManager()
        self.llm_client: Optional[LLMClient] = None
        self.session: Optional[PromptSession] = None

    def setup(self, interactive: bool) -> None:
        try:
            openai_config = self.config_manager.get_openai_config()
            self.llm_client = LLMClient(openai_config)
            history_file = self.config_manager.get_history_file()
            self.session = PromptSession(history=FileHistory(str(history_file))) if interactive else None
        except Exception as e:
            print(f"Error during setup: {e}", file=sys.stderr)
            sys.exit(1)

    def get_system_prompt(self, prompt_name: str) -> str:
        prompt_config = self.config_manager.get_prompt_by_name(prompt_name)
        if not prompt_config:
            return ""
        
        prompt_text = prompt_config.get("prompt", "")
        
        # Handle files element if present
        files = prompt_config.get("files", [])
        if files:
            file_contents = []
            for file_path in files:
                try:
                    expanded_path = os.path.expandvars(os.path.expanduser(file_path))
                    with open(expanded_path, 'r', encoding='utf-8') as f:
                        file_contents.append(f"\n--- Content from {expanded_path} ---\n{f.read()}")
                except Exception as e:
                    print(f"Warning: Could not read file1 {expanded_path}: {e}", file=sys.stderr)
            
            if file_contents:
                prompt_text = prompt_text + ''.join(file_contents)
        
        return prompt_text or ""

    def run(self, interactive: bool, system_prompt_name: str, user_prompt: str) -> None:
        system_prompt = self.get_system_prompt(system_prompt_name)

        try:
            while True:
                try:
                    user_input = user_prompt 
                    if not user_prompt:
                        if self.session is None:
                            user_input = input("> ").strip()
                        else:
                            user_input = self.session.prompt("> ").strip()
                    user_prompt = ""  # Clear after first use

                    if not user_input:
                        break

                    # Check for exit commands
                    if user_input.lower() in ["exit", "quit", "q"]:
                        print("Goodbye!")
                        break

                    # Process the prompt (handle files and std input)
                    processed_prompt = PromptProcessor.process_prompt(user_input)

                    # Send to LLM
                    response = self.llm_client.send_message(
                        processed_prompt,
                        system_prompt=system_prompt if system_prompt else None,
                    )
                    print(response)

                    if not interactive:
                        break

                except KeyboardInterrupt:
                    print("\nBye!")
                    break
                except EOFError:
                    print("\nBye!")
                    break
                except Exception as e:
                    print(f"Error: {e}", file=sys.stderr)
                    print()

        except Exception as e:
            print(f"Fatal error: {e}", file=sys.stderr)
            sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="AI Chat Client - Command line ChatGPT interface",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s -i                       # Interactive mode
  %(prog)s -sp system_prompt        # Use system prompt configuration
  %(prog)s "Summarize @readme.txt"  # Include file content
  %(prog)s "Explain @@"             # Include standard input content
        """,
    )

    parser.add_argument(
        "-i", "--interactive", action="store_true", help="Interactive mode"
    )

    # Prompt configuration
    parser.add_argument(
        "-sp",
        "--system-prompt",
        default="default",
        help="Named system prompt from .ai_config.json (default: default)",
    )

    parser.add_argument("prompt", nargs="*", help="Prompt")
    args = parser.parse_args()

    app = ChatApp()
    interactive = args.interactive and sys.stdin.isatty()
    app.setup(interactive)
    app.run(interactive, args.system_prompt, " ".join(args.prompt) if args.prompt else "")

if __name__ == "__main__":
    main()
