Create a python command line app that behaves as a ChatGPT client 
1) It has two modes:
- interactive: commnand line option -i , default mode. You write your prompt and then the reponse from chatgpt is displayed. It then waits for a new prompt. 
- non interactive: commnand line option -ni, exists after first prompt
2) It saves a history of user prompts that can be accessed using the up and down keys. History is saved accros runs in .ai_history file
3) One configuration .ai_config.json file, format:  {prompts: [{name:"default" , prompt: ""}]}. The named prompt is prepended to the initial prompt from the user. prompt can be selected by -p: name
4) I can add a file or files for context if a word starts with #. For example: "Make a summary of #test.txt". It can be a absolute or relative path. It can contain Globbing or multiple files separated by ;.
5) I can add the clipboard to the prompt with ##

Coding Guidelines:
- Use one python file for all chatgpt interaction. It can be replaced with another LLM in the future.
- Make it modular
- Follow all python PEP rules
- Use latest openai python library