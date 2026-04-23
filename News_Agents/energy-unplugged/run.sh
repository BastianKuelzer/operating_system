#!/bin/bash
# Wrapper so launchd/cron can find python3 and env vars
source ~/.zshrc 2>/dev/null || true
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"
python3 summarize.py >> "$SCRIPT_DIR/run.log" 2>&1
