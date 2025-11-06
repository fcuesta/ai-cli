import glob
import os
import sys

class PromptProcessor:
    @staticmethod
    def process_prompt(prompt: str) -> str:
        # Handle file references (#filename)
        words = prompt.split()
        for i, word in enumerate(words):
            if word.startswith("@@"):
                words[i] = ""
                std_input = PromptProcessor.read_stdin()
                words[i] = f"\n\nInput:\n{std_input}\n"
            elif word.startswith("@") and not word.startswith("@@"):
                file_pattern = word[1:]  # Remove the @ prefix
                file_content = PromptProcessor._read_files(file_pattern)
                words[i] = f"\n\nFile content from '{file_pattern}':\n{file_content}\n"
        
        return " ".join(words)
    
    @staticmethod
    def read_stdin() -> str:
        std_input = ""
        if not sys.stdin.isatty():
            std_input = sys.stdin.read()
        return std_input

    @staticmethod
    def _read_files(file_pattern: str) -> str:
        contents = []
        
        # Handle semicolon-separated files
        patterns = [pattern.strip() for pattern in file_pattern.split(";")]
        
        for pattern in patterns:
            if not pattern:
                continue
                
            # Convert to absolute path if relative
            if not os.path.isabs(pattern):
                pattern = os.path.join(os.getcwd(), pattern)
            
            try:
                # Handle glob patterns
                matching_files = glob.glob(pattern)
                
                if not matching_files:
                    # If no glob matches, try as literal filename
                    if os.path.exists(pattern):
                        matching_files = [pattern]
                    else:
                        contents.append(f"[File not found: {pattern}]")
                        continue
                
                for file_path in sorted(matching_files):
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            file_content = f.read()
                        contents.append(f"--- {os.path.basename(file_path)} ---\n{file_content}")
                    except Exception as e:
                        contents.append(f"[Error reading {file_path}: {str(e)}]")
                        
            except Exception as e:
                contents.append(f"[Error processing pattern {pattern}: {str(e)}]")
        
        return "\n\n".join(contents) if contents else "[No files found]"

