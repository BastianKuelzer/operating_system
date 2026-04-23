#!/bin/zsh
# Wrapper for Energate Morning News Agent
# Sourced by cron — loads user env before calling the Python agent

source "$HOME/.zshrc" 2>/dev/null || true

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LOG="$HOME/Library/Logs/energate_agent.log"
mkdir -p "$(dirname "$LOG")"

echo "──────────────────────────────────" >> "$LOG"
echo "$(date '+%Y-%m-%d %H:%M:%S') Starting Energate News Agent" >> "$LOG"

/usr/bin/python3 "$SCRIPT_DIR/energate_news_agent.py" >> "$LOG" 2>&1
EXIT_CODE=$?

if [ $EXIT_CODE -ne 0 ]; then
    echo "$(date '+%Y-%m-%d %H:%M:%S') ERROR: agent exited with code $EXIT_CODE" >> "$LOG"
    osascript -e 'display notification "Check ~/Library/Logs/energate_agent.log for details" with title "Energate Agent Failed" sound name "Basso"' 2>/dev/null || true
fi

echo "$(date '+%Y-%m-%d %H:%M:%S') Done (exit $EXIT_CODE)" >> "$LOG"
