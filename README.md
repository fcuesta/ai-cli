# TODO

pip install git+https://github.com/fcuesta/ai-cli.git 
pip install git+https://github.com/fcuesta/ai-cli.git --force-reinstall -vvv


# AI Chat Client

A modular Python command line application that behaves as a ChatGPT client with interactive and non-interactive modes.

## Features

- **Two modes**: Interactive (default) and non-interactive
- **History support**: Up/down arrow keys to access previous prompts (saved in `.ai_history`)
- **Configuration**: Named prompts in `.ai_config.json`
- **File integration**: Include file content with `#filename` syntax
- **Clipboard support**: Include clipboard content with `##`
- **Modular design**: Easy to replace LLM backend

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set your OpenAI API key:
```bash
export OPENAI_API_KEY="your-api-key-here"
```

## Usage

### Interactive Mode (Default)
```bash
python chat_app.py
# or explicitly
python chat_app.py -i
```

### Non-Interactive Mode
```bash
python chat_app.py -ni "Your prompt here"
```

### Using Named Prompts
```bash
python chat_app.py -p coder -ni "Write a Python function to sort a list"
```

### File References
Include file content in your prompt:
```bash
python chat_app.py -ni "Summarize #README.md"
python chat_app.py -ni "Explain #*.py"
python chat_app.py -ni "Compare #file1.txt;file2.txt"
```

### Clipboard Integration
Include clipboard content:
```bash
python chat_app.py -ni "Explain ##"
```

## Configuration

The application uses `.ai_config.json` for configuration:

```json
{
  "prompts": {
    "default": {
      "prompt": "Provide clear concise minimal a..."
    },
    "linux": {
      "prompt": "Provide clear concise minimal a..."
    },
  }
}
```

## Command Line Options

- `-i, --interactive`: Interactive mode (default)
- `-ni, --non-interactive PROMPT`: Non-interactive mode
- `-p, --prompt NAME`: Named prompt from config (default: "default")

## Examples

```bash
# Basic interactive mode
python chat_app.py

# Non-interactive with file content
python chat_app.py -ni "Make a summary of #test.txt"

# Use custom prompt configuration  
python chat_app.py -sp writer -ni "Improve this text: ##"

# Multiple files with globbing
python chat_app.py -ni "Analyze #src/*.py and #tests/*.py"
```

## Files

- `chat_app.py`: Main application entry point
- `llm_client.py`: OpenAI/ChatGPT client (replaceable)
- `config_manager.py`: Configuration file management  
- `prompt_processor.py`: File and clipboard processing
- `shell_history.py`: Shell history integration
- `.ai_config.json`: Configuration file
- `.ai_history`: Command history file
- Type your messages and receive responses
- Type `reset` to clear conversation history
- Type `exit` or `quit` to end the session

### OUTDATED DOC
### Shell Mode
```bash
./chat_app.py -s
# or
./chat_app.py --shell
```

In shell mode:
- Describe what you want to do in natural language
- Receive a shell command that accomplishes the task
- Commands are automatically saved to your shell history

### File References

Include file content in your prompts using `#`:

```bash
> Summarize #document.txt
> Compare #file1.txt and #file2.txt
> Analyze all Python files #*.py
> Review #src/main.py;tests/test.py
```

Supported patterns:
- Single file: `#filename.txt`
- Absolute path: `#/path/to/file.txt`
- Relative path: `#./relative/path.txt`
- Glob patterns: `#*.py`, `#src/**/*.js`
- Multiple files: `#file1.txt;file2.txt;file3.txt`

### Clipboard Integration

Include clipboard content using `##`:

```bash
> Fix this code ##
> Translate this text ##
```

**Note**: Requires `xclip` or `xsel` on Linux:
```bash
sudo apt-get install xclip
# or
sudo apt-get install xsel
```

## Configuration Files

### config.ini
Main configuration file containing OpenAI API credentials and model settings.

### .chat-prompt
System prompt prepended to all chat mode conversations. Customize this to change the assistant's behavior in chat mode.

### .shell-prompt
System prompt prepended to shell command generation requests. Should instruct the model to output only commands.

## Project Structure

```
chat_app.py           - Main application and CLI interface
llm_client.py         - ChatGPT/LLM interaction module (replaceable)
config_manager.py     - Configuration file management
prompt_processor.py   - File and clipboard content processing
shell_history.py      - Shell history integration
config.ini            - API configuration
.chat-prompt          - Chat mode system prompt
.shell-prompt         - Shell mode system prompt
requirements.txt      - Python dependencies
```

## Module Design

The application is designed with modularity in mind:

- **llm_client.py**: Isolated LLM interaction. Can be replaced with other providers (Claude, Llama, etc.) by implementing the same interface.
- **config_manager.py**: Centralized configuration management
- **prompt_processor.py**: Handles all prompt transformations (file/clipboard inclusion)
- **shell_history.py**: Shell-specific operations
- **chat_app.py**: Main orchestration and CLI

## PEP Compliance

This project follows Python PEP standards:
- PEP 8: Code style and formatting
- PEP 257: Docstring conventions
- PEP 484: Type hints

## Examples

### Chat Mode Example
```
> What is the capital of France?
The capital of France is Paris.

> Tell me more about it
Paris is the largest city in France...
```

### Shell Mode Example
```
> find all Python files modified in the last 7 days
find . -name "*.py" -type f -mtime -7

> compress the logs directory
tar -czf logs.tar.gz logs/
```

### With File Context
```
> Summarize #README.md
[Summary of README.md content...]

> Find bugs in #src/*.py
[Analysis of all Python files in src/...]
```

## License

MIT License


### pack to one file
cd ./ai-prompt
pyinstaller --onefile chat_app.py