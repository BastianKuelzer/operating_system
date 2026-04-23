# Podcast Summarizer

One script that monitors three energy podcasts, downloads new episodes, transcribes the audio, and saves structured markdown summaries per podcast.

## Podcasts

| Folder | Podcast | RSS |
|--------|---------|-----|
| `energy-unplugged/` | Energy Unplugged by Aurora | podbean.com |
| `redefining-energy/` | Redefining Energy | spreaker.com |
| `energy-gang/` | The Energy Gang | art19.com |

Each podcast folder holds its own `.state.json` (tracks processed episodes) and receives its own `summaries/` and `transcripts/` output directories — both excluded from git.

## What it does per episode

1. Fetches the RSS feed and filters out already-processed episodes
2. Downloads the audio and transcribes it (local Whisper → OpenAI Whisper API → show notes fallback)
3. Summarizes with Claude into **Overview · Key Topics · Key Insights**
4. Saves `summaries/YYYY-MM-DD-title.md` and (if transcribed) `transcripts/YYYY-MM-DD-title.md`
5. Updates `.state.json` so the episode is never processed again

## Setup

```bash
cd News_Agents/podcasts
pip install -r requirements.txt
export ANTHROPIC_API_KEY=your_key_here
# Optional — for OpenAI Whisper API fallback:
export OPENAI_API_KEY=your_key_here
```

## Run manually

```bash
python3 summarize.py
```

## Schedule automatically (macOS)

```bash
chmod +x run.sh
crontab -e
# Run daily at 07:00:
0 7 * * * /path/to/News_Agents/podcasts/run.sh
```

Logs are written to `run.log` next to the script.

## Adding a podcast

Add an entry to the `PODCASTS` dict in `summarize.py`:

```python
"my-podcast": {
    "name": "My Podcast Name",
    "rss": "https://example.com/feed.xml",
},
```

Then create the folder so the state file has somewhere to live:

```bash
mkdir News_Agents/podcasts/my-podcast
```

## Transcription options

| Option | Requirement | Notes |
|--------|-------------|-------|
| Local Whisper | `pip install openai-whisper` | Free, GPU helps with speed |
| OpenAI Whisper API | `OPENAI_API_KEY` | Fast, costs per minute |
| Show notes fallback | Nothing | Summary only, no transcript saved |
