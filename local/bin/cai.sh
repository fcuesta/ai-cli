#!/bin/bash
prompt="$*"
xclip -selection clipboard -o | ai-cli -i "$prompt" | tee >(xclip -selection clipboard -i)