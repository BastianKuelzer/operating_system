#!/usr/bin/env python3
"""
Energy Podcast Summarizer
Fetches new episodes from configured podcasts, transcribes, and saves markdown summaries.

Requirements: pip install feedparser requests anthropic openai-whisper
API key needed: ANTHROPIC_API_KEY
"""

import json
import os
import re
import tempfile
from datetime import datetime
from pathlib import Path

import anthropic
import feedparser
import requests

BASE_DIR = Path(__file__).parent

PODCASTS = {
    "energy-unplugged": {
        "name": "Energy Unplugged by Aurora",
        "rss": "https://feed.podbean.com/aercommercial/feed.xml",
    },
    "redefining-energy": {
        "name": "Redefining Energy",
        "rss": "https://www.spreaker.com/show/3170008/episodes/feed",
    },
    "energy-gang": {
        "name": "The Energy Gang",
        "rss": "https://rss.art19.com/the-energy-gang",
    },
}


def load_state(podcast_dir: Path) -> dict:
    state_file = podcast_dir / ".state.json"
    if state_file.exists():
        return json.loads(state_file.read_text())
    return {"processed": []}


def save_state(podcast_dir: Path, state: dict):
    podcast_dir.mkdir(exist_ok=True)
    (podcast_dir / ".state.json").write_text(json.dumps(state, indent=2))


def fetch_feed(rss_url: str) -> list[dict]:
    feed = feedparser.parse(rss_url)
    episodes = []
    for entry in feed.entries:
        audio_url = None
        for enclosure in entry.get("enclosures", []):
            if "audio" in enclosure.get("type", ""):
                audio_url = enclosure.get("url")
                break
        if not audio_url:
            for link in entry.get("links", []):
                if link.get("type", "").startswith("audio"):
                    audio_url = link["href"]
                    break

        episodes.append({
            "id": entry.get("id") or entry.get("link", ""),
            "title": entry.get("title", "Untitled"),
            "published": entry.get("published", ""),
            "description": entry.get("summary", ""),
            "audio_url": audio_url,
            "duration": entry.get("itunes_duration", ""),
        })
    return episodes


def download_audio(url: str, dest: Path) -> bool:
    try:
        with requests.get(url, stream=True, timeout=600) as r:
            r.raise_for_status()
            with open(dest, "wb") as f:
                for chunk in r.iter_content(chunk_size=65536):
                    f.write(chunk)
        return True
    except Exception as e:
        print(f"  Download failed: {e}")
        return False


def transcribe_audio(audio_path: Path) -> str:
    try:
        import whisper
        print("  Transcribing with local Whisper...")
        model = whisper.load_model("base")
        result = model.transcribe(str(audio_path))
        return result["text"]
    except ImportError:
        pass
    except Exception as e:
        print(f"  Local Whisper failed: {e}")

    api_key = os.environ.get("OPENAI_API_KEY")
    if api_key:
        try:
            import openai
            client = openai.OpenAI(api_key=api_key)
            with open(audio_path, "rb") as f:
                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=f,
                    response_format="text",
                )
            return transcript
        except Exception as e:
            print(f"  OpenAI Whisper API failed: {e}")

    print("  No transcription available — using show notes.")
    return ""


def summarize(podcast_name: str, episode: dict, transcript: str, client: anthropic.Anthropic) -> str:
    source = "Full transcript" if transcript else "Show notes"
    content = transcript if transcript else episode["description"]

    prompt = f"""You are summarizing an episode of "{podcast_name}", a podcast covering energy markets, renewables, and the energy transition.

Episode title: {episode['title']}
{source}:
{content}

Write a concise markdown summary with exactly this structure:

## Overview
2–3 sentence summary of what this episode is about.

## Key Topics
- Topic 1
- Topic 2
- Topic 3
(etc.)

## Key Insights
- Insight 1
- Insight 2
- Insight 3
(3–5 bullets, focused on actionable or notable takeaways for energy professionals)

Be specific and factual. Avoid filler phrases like "the hosts discuss" — just state the substance."""

    message = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=1500,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    return text.strip("-")[:70]


def parse_date(published: str) -> str:
    formats = ["%a, %d %b %Y %H:%M:%S %z", "%a, %d %b %Y %H:%M:%S %Z"]
    for fmt in formats:
        try:
            return datetime.strptime(published, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return datetime.now().strftime("%Y-%m-%d")


def save_files(podcast_dir: Path, podcast_name: str, episode: dict, summary: str, transcript: str):
    summaries_dir = podcast_dir / "summaries"
    transcripts_dir = podcast_dir / "transcripts"
    summaries_dir.mkdir(exist_ok=True)
    transcripts_dir.mkdir(exist_ok=True)

    date_str = parse_date(episode["published"])
    slug = slugify(episode["title"])

    summary_md = f"""# {episode['title']}

**Podcast:** {podcast_name}
**Published:** {episode['published']}
**Duration:** {episode.get('duration', 'N/A')}

---

{summary}

---
*Generated {datetime.now().strftime('%Y-%m-%d')}*
"""
    summary_path = summaries_dir / f"{date_str}-{slug}.md"
    summary_path.write_text(summary_md)
    print(f"  Saved summary → {summary_path.name}")

    if transcript:
        transcript_md = f"""# {episode['title']} — Full Transcript

**Podcast:** {podcast_name}
**Published:** {episode['published']}
**Duration:** {episode.get('duration', 'N/A')}

---

{transcript}
"""
        transcript_path = transcripts_dir / f"{date_str}-{slug}.md"
        transcript_path.write_text(transcript_md)
        print(f"  Saved transcript → {transcript_path.name}")


def process_podcast(slug: str, config: dict, client: anthropic.Anthropic):
    podcast_dir = BASE_DIR / slug
    print(f"\n{'='*50}")
    print(f"  {config['name']}")
    print(f"{'='*50}")

    state = load_state(podcast_dir)
    processed = set(state["processed"])

    episodes = fetch_feed(config["rss"])
    new_episodes = [e for e in episodes if e["id"] not in processed]

    if not new_episodes:
        print("  No new episodes.")
        return

    print(f"  Found {len(new_episodes)} new episode(s).")

    for episode in new_episodes:
        print(f"\n  Processing: {episode['title']}")
        transcript = ""

        if episode.get("audio_url"):
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
                tmp_path = Path(tmp.name)
            print("  Downloading audio...")
            if download_audio(episode["audio_url"], tmp_path):
                transcript = transcribe_audio(tmp_path)
                tmp_path.unlink(missing_ok=True)

        summary = summarize(config["name"], episode, transcript, client)
        save_files(podcast_dir, config["name"], episode, summary, transcript)

        processed.add(episode["id"])
        state["processed"] = list(processed)
        save_state(podcast_dir, state)


def main():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] Podcast summarizer starting...")
    client = anthropic.Anthropic()
    for slug, config in PODCASTS.items():
        process_podcast(slug, config, client)
    print("\nAll done.")


if __name__ == "__main__":
    main()
