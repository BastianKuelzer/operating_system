# Energate Morning News Agent

Fetches the latest articles from the [energate messenger](https://www.energate.de/) RSS feed, generates a structured English morning briefing with Claude, and saves it to `~/Documents/Energate News/`. On macOS, it also sends a desktop notification and opens the report automatically.

## What it does

1. Pulls the 15 most recent articles from the energate RSS feed
2. Sends them to Claude for a structured briefing:
   - **Top 3 headlines** — market impact in one sentence each
   - **Key themes** — 3–5 overarching topics
   - **Market watch** — price signals, regulatory moves, supply/demand shifts
   - **Quick scan** — remaining articles with one-line takeaways
3. Saves the briefing to `~/Documents/Energate News/Energate_News_YYYY-MM-DD.md`
4. Sends a macOS notification and opens the file

## Setup

```bash
cd News_Agents/energate
pip install -r requirements.txt
export ANTHROPIC_API_KEY=your_key_here
```

> Note: energate messenger is a German-language publication. The RSS feed requires a valid subscription to return full article content. The agent still works with headlines and summaries on a free/limited feed.

## Run manually

```bash
python3 energate_news_agent.py
```

## Schedule automatically (macOS)

Make the wrapper executable and add it to cron:

```bash
chmod +x run_energate_agent.sh
crontab -e
# Add this line to run daily at 07:30:
30 7 * * * /path/to/News_Agents/energate/run_energate_agent.sh
```

Logs are written to `~/Library/Logs/energate_agent.log`.

## Output

- `~/Documents/Energate News/Energate_News_YYYY-MM-DD.md` — daily briefing
- `~/Library/Logs/energate_agent.log` — execution log
