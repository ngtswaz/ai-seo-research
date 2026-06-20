"""
YouTube Transcript Collector
============================
Fetches transcripts via the Supadata API (https://supadata.ai),
which handles PO tokens and cookie requirements automatically.

Saves to: research/youtube-transcripts/<author>/<video_id>_<title>.md

Requirements:
    pip3 install requests

Usage:
    export SUPADATA_API_KEY="your_key_here"
    python3 scripts/fetch_youtube_transcripts.py [--dry-run] [--expert SLUG]
"""

import argparse
import os
import re
import sys
import time
from pathlib import Path
from typing import Optional, Dict

try:
    import requests
except ImportError:
    sys.exit("Missing: run  pip3 install requests")

# ── Config ────────────────────────────────────────────────────────────────────

API_KEY    = os.environ.get("SUPADATA_API_KEY", "")
REPO_ROOT  = Path(__file__).resolve().parent.parent
OUTPUT_DIR = REPO_ROOT / "research" / "youtube-transcripts"
SLEEP      = 1.5   # seconds between API calls

# ── Hand-picked videos per expert ────────────────────────────────────────────

EXPERTS: Dict[str, Dict] = {
    "lily-ray": {
        "display_name": "Lily Ray",
        "videos": [
            {"url": "https://www.youtube.com/watch?v=mgI1U7XPsUA", "title": "How SEO is Evolving in 2025 - Lily Ray Talks AI Reddit and Ranking"},
            {"url": "https://www.youtube.com/watch?v=f84ovVChEh4", "title": "AI-Driven SEO Revolution - Lily Ray on Future of Discoverability"},
        ],
    },
    "bernard-huang": {
        "display_name": "Bernard Huang (Clearscope)",
        "videos": [
            {"url": "https://www.youtube.com/watch?v=3aEDx9J5U9k", "title": "Building AI-Powered SEO Tools - Bernard Huang Clearscope"},
            {"url": "https://www.youtube.com/watch?v=f84ovVChEh4", "title": "AI-Driven SEO Revolution - Bernard Huang Clearscope"},
        ],
    },
    "kevin-indig": {
        "display_name": "Kevin Indig",
        "videos": [
            {"url": "https://www.youtube.com/watch?v=Vt_C1pEfNd8", "title": "Preparing for Organic Growth in 2025 - Kevin Indig AirOps"},
        ],
    },
    "aleyda-solis": {
        "display_name": "Aleyda Solis",
        "videos": [
            {"url": "https://www.youtube.com/watch?v=yesGVbDGdIM", "title": "AI Content Strategy and SEO Insights - Aleyda Solis Innovation Visual"},
            {"url": "https://www.youtube.com/watch?v=mgI1U7XPsUA", "title": "Crawling Mondays SEO AI Search 2025 - Aleyda Solis"},
        ],
    },
    "nate-matherson": {
        "display_name": "Nate Matherson",
        "videos": [
            {"url": "https://www.youtube.com/watch?v=IKcnYZ459kw", "title": "SEO and Content Marketing for Startups - Nate Matherson VectorShift"},
        ],
    },
    "ryan-law": {
        "display_name": "Ryan Law (Ahrefs)",
        "videos": [
            {"url": "https://www.youtube.com/watch?v=D7LBx8RFOcQ", "title": "AI Writing at Scale Ahrefs Step-by-Step Workflow - Ryan Law"},
            {"url": "https://www.youtube.com/watch?v=iVZrVeESnFQ", "title": "How to Automate Blog Writing with AI Keyword to Published - Ryan Law Ahrefs"},
        ],
    },
    "ross-simmonds": {
        "display_name": "Ross Simmonds",
        "videos": [
            {"url": "https://www.youtube.com/watch?v=pGc3bTjliKY", "title": "Disrupt Content Economy with One-Click AI Tool - Surfer SEO Ross Simmonds"},
            {"url": "https://www.youtube.com/watch?v=3_huJv4Xp6E", "title": "Product Marketing to 15M ARR - Tomasz Niezgoda Surfer"},
        ],
    },
    "koray-tugberk-gubur": {
        "display_name": "Koray Tugberk GUBUR",
        "videos": [
            {"url": "https://www.youtube.com/watch?v=X_ou1eO28gE", "title": "Exploring Holistic SEO Semantic SEO and Topical Authority - Koray Tugberk"},
            {"url": "https://www.youtube.com/watch?v=pIKfKowzauQ", "title": "How Topical Authority SEO Works - Koray Tugberk GUBUR"},
        ],
    },
    "tomasz-niezgoda": {
        "display_name": "Tomasz Niezgoda (Surfer SEO)",
        "videos": [
            {"url": "https://www.youtube.com/watch?v=pGc3bTjliKY", "title": "Disrupt Content Economy with One-Click AI Tool - Tomasz Niezgoda Surfer"},
            {"url": "https://www.youtube.com/watch?v=3_huJv4Xp6E", "title": "Product Marketing to 15M ARR Tomasz Niezgoda Surfer SEO"},
        ],
    },
    "eli-schwartz": {
        "display_name": "Eli Schwartz",
        "videos": [
            {"url": "https://www.youtube.com/watch?v=x5CgYCRLgbc", "title": "Product-Led SEO in AI Era - Eli Schwartz and Surfer"},
        ],
    },
}

# ── Helpers ───────────────────────────────────────────────────────────────────

def slugify(text: str, max_len: int = 70) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text[:max_len].strip("-")


def video_id_from_url(url: str) -> str:
    m = re.search(r"v=([A-Za-z0-9_-]{11})", url)
    return m.group(1) if m else slugify(url)[:11]


def already_collected(author: str, vid_id: str) -> bool:
    author_dir = OUTPUT_DIR / author
    return any(author_dir.glob(f"{vid_id}_*.md")) if author_dir.exists() else False


def fetch_transcript(video_id: str) -> Optional[str]:
    """Fetch transcript via Supadata API."""
    url = "https://api.supadata.ai/v1/youtube/transcript"
    headers = {"x-api-key": API_KEY}
    params  = {"videoId": video_id, "text": "true"}  # text=true returns plain text

    try:
        resp = requests.get(url, headers=headers, params=params, timeout=30)
        if resp.status_code == 200:
            data = resp.json()
            # Supadata returns {"content": "...", "lang": "en", ...}
            text = data.get("content", "") or data.get("transcript", "")
            if isinstance(text, list):
                # Some responses return a list of segment objects
                text = " ".join(s.get("text", "") for s in text)
            text = str(text).strip()
            return text if len(text) > 100 else None
        elif resp.status_code == 404:
            print("    ✗ No transcript found (video may have no captions)")
            return None
        elif resp.status_code == 401:
            sys.exit("\nERROR: Invalid Supadata API key. Check your key and try again.\n")
        else:
            print(f"    ⚠ API error {resp.status_code}: {resp.text[:200]}")
            return None
    except requests.RequestException as e:
        print(f"    ⚠ Request error: {e}")
        return None


def save_transcript(author: str, vid_id: str, title: str, url: str, transcript: str) -> None:
    author_dir = OUTPUT_DIR / author
    author_dir.mkdir(parents=True, exist_ok=True)
    filepath = author_dir / f"{vid_id}_{slugify(title)}.md"
    filepath.write_text(f"""---
author: {author}
video_id: {vid_id}
title: "{title}"
url: {url}
collected_by: fetch_youtube_transcripts.py (Supadata API)
---

# {title}

**URL:** {url}

## Transcript

{transcript}
""", encoding="utf-8")
    print(f"    ✓ Saved → research/youtube-transcripts/{author}/{filepath.name}")


# ── Main ──────────────────────────────────────────────────────────────────────

def process_expert(slug: str, config: Dict, dry_run: bool) -> Dict:
    print(f"\n{'─'*60}")
    print(f"  {config['display_name']}")
    print(f"{'─'*60}")

    videos = config["videos"]
    print(f"    {len(videos)} video(s) queued")
    saved = skipped = 0

    for v in videos:
        url    = v["url"]
        title  = v["title"]
        vid_id = video_id_from_url(url)

        print(f"\n    [{vid_id}] {title[:65]}")
        print(f"    {url}")

        if dry_run:
            print("    (dry-run — skipping fetch)")
            continue

        if already_collected(slug, vid_id):
            print("    ↩ Already collected")
            skipped += 1
            continue

        transcript = fetch_transcript(vid_id)
        time.sleep(SLEEP)

        if transcript:
            save_transcript(slug, vid_id, title, url, transcript)
            saved += 1
        else:
            skipped += 1

    return {"expert": slug, "found": len(videos), "saved": saved, "skipped": skipped}


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch YouTube transcripts via Supadata API")
    parser.add_argument("--dry-run", action="store_true", help="List videos without fetching")
    parser.add_argument("--expert", metavar="SLUG", help="Only process one expert")
    args = parser.parse_args()

    if not API_KEY and not args.dry_run:
        sys.exit(
            "\nERROR: SUPADATA_API_KEY not set.\n"
            "1. Sign up free at https://supadata.ai\n"
            "2. Copy your API key\n"
            "3. Run: export SUPADATA_API_KEY='your_key_here'\n"
        )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if args.expert:
        if args.expert not in EXPERTS:
            sys.exit(f"Unknown slug '{args.expert}'. Options: {', '.join(EXPERTS)}")
        experts_to_run = {args.expert: EXPERTS[args.expert]}
    else:
        experts_to_run = EXPERTS

    mode = "DRY RUN" if args.dry_run else "COLLECTING"
    print(f"\n{'='*60}")
    print(f"  YouTube Transcript Collector — {mode}")
    print(f"  Experts: {len(experts_to_run)}")
    print(f"{'='*60}")

    results = []
    for slug, config in experts_to_run.items():
        results.append(process_expert(slug, config, args.dry_run))

    print(f"\n\n{'='*60}")
    print("  SUMMARY")
    print(f"{'='*60}")
    total_saved = total_skipped = 0
    for r in results:
        print(f"  {r['expert']:<32} found={r['found']}  saved={r['saved']}  skipped={r['skipped']}")
        total_saved   += r["saved"]
        total_skipped += r["skipped"]
    print(f"\n  Total saved: {total_saved}  |  Skipped: {total_skipped}")
    print()


if __name__ == "__main__":
    main()
