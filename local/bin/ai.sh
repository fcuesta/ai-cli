#!/bin/bash
prompt="$*"
command=$(ai-cli -i "$prompt")
echo "$command"

# --- Add to shell history ---
# This only works if the script runs inside an interactive bash shell
if [ -n "$BASH_VERSION" ]; then
  history -s "$command"
fi