# Energy Unplugged — Podcast Summarizer

Automatically fetches new episodes of the [Energy Unplugged by Aurora](https://feed.podbean.com/aercommercial/feed.xml) podcast, transcribes the audio, and saves a structured markdown summary to `summaries/`.

## What it does

1. Reads the RSS feed for new episodes not yet processed
2. Downloads the audio and transcribes it (local Whisper or OpenAI Whisper API)
3. Summarizes with Claude into Overview, Key Topics, and Key Insights
4. Saves the summary to `summaries/YYYY-MM-DD-episode-title.md`
5. Tracks processed episodes in `.state.json` so it never re-runs the same episode

## Setup

```bash
cd News_Agents/energy-unplugged
pip install -r requirements.txt
export ANTHROPIC_API_KEY=your_key_here
# Optional — for better transcription quality via OpenAI Whisper API:
export OPENAI_API_KEY=your_key_here
```

## Run manually

```bash
python3 summarize.py
```

## Schedule automatically (macOS)

Make the wrapper executable and add it to cron:

```bash
chmod +x run.sh
crontab -e
# Add this line to run daily at 07:00:
0 7 * * * /path/to/News_Agents/energy-unplugged/run.sh
```

## Transcription options

| Option | Requirement | Quality |
|--------|-------------|---------|
| Local Whisper (`openai-whisper`) | No API key, GPU helps | Good |
| OpenAI Whisper API | `OPENAI_API_KEY` | Good |
| Show notes fallback | Nothing | Summary only |

The script tries local Whisper first, then OpenAI API, then falls back to show notes.

## Output

- `summaries/` — one markdown file per episode with Overview, Key Topics, Key Insights
- `transcripts/` — full transcripts (only when audio transcription succeeds)
- `run.log` — execution log
