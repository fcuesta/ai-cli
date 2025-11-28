#!/bin/bash
prompt="$*"
command=$(curl -sS https://api.openai.com/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer redacted" \
  -d "{
    \"model\": \"gpt-4-turbo\",
    \"messages\": [
      {
        \"role\": \"system\",
        \"content\": \"You are a Linux terminal command generator. Output ONLY the exact command with no explanation, no markdown, and no additional text.\"
      },
      {
        \"role\": \"user\",
        \"content\": \"$prompt\"
      }
    ]
  }" | jq -r '.choices[0].message.content')

echo "$command"

# --- Add to shell history ---
# This only works if the script runs inside an interactive bash shell
if [ -n "$BASH_VERSION" ]; then
  history -s "$command"
fi
