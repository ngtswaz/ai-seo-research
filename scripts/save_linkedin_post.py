"""
LinkedIn Post Saver
===================
Formats a manually collected LinkedIn post and saves it to the correct
folder under research/linkedin-posts/<author>/.

LinkedIn blocks API scraping, so collection is manual — but this script
ensures every saved post has a consistent structure for later analysis.

Usage:
    python scripts/save_linkedin_post.py

The script will interactively ask for:
    - Author (pick from list)
    - Post URL
    - Date (YYYY-MM-DD)
    - Approximate like count
    - Topic tags
    - Post text (paste, end with a line containing only "END")
    - Why you saved it (1-2 sentences)

Output is saved to:
    research/linkedin-posts/<author>/<date>-<slug>.md
"""

import re
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = REPO_ROOT / "research" / "linkedin-posts"

EXPERTS = {
    "1":  ("lily-ray",           "Lily Ray"),
    "2":  ("bernard-huang",      "Bernard Huang"),
    "3":  ("kevin-indig",        "Kevin Indig"),
    "4":  ("aleyda-solis",       "Aleyda Solis"),
    "5":  ("nate-matherson",     "Nate Matherson"),
    "6":  ("ryan-law",           "Ryan Law"),
    "7":  ("ross-simmonds",      "Ross Simmonds"),
    "8":  ("koray-tugberk-gubur","Koray Tugberk GUBUR"),
    "9":  ("tomasz-niezgoda",    "Tomasz Niezgoda"),
    "10": ("eli-schwartz",       "Eli Schwartz"),
}

TOPIC_SUGGESTIONS = [
    "ai-seo", "content-production", "geo", "topical-authority",
    "content-quality", "ai-tools", "b2b-saas", "programmatic-seo",
    "content-distribution", "aeo", "llm-citations", "workflow",
]


def slugify(text: str, max_len: int = 60) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    return text[:max_len].strip("-")


def prompt(label: str, required: bool = True) -> str:
    while True:
        val = input(f"  {label}: ").strip()
        if val or not required:
            return val
        print("  (required — please enter a value)")


def pick_expert() -> tuple[str, str]:
    print("\n  Choose expert:")
    for k, (slug, name) in EXPERTS.items():
        print(f"    {k:>2}. {name}")
    while True:
        choice = input("  Enter number: ").strip()
        if choice in EXPERTS:
            return EXPERTS[choice]
        print("  Invalid choice.")


def collect_post_text() -> str:
    print("  Paste the full post text below.")
    print("  When done, enter a line with only END and press Return.\n")
    lines = []
    while True:
        line = input()
        if line.strip().upper() == "END":
            break
        lines.append(line)
    return "\n".join(lines).strip()


def main() -> None:
    print("\n" + "="*60)
    print("  LinkedIn Post Saver")
    print("="*60)

    slug, display_name = pick_expert()

    url = prompt("Post URL (linkedin.com/posts/...)")
    post_date = prompt(f"Date (YYYY-MM-DD) [default: {date.today()}]", required=False) or str(date.today())
    likes = prompt("Approximate likes (e.g. 450)", required=False) or "unknown"

    print(f"\n  Topic tag suggestions: {', '.join(TOPIC_SUGGESTIONS)}")
    tags_raw = prompt("Topic tags (comma-separated)")
    tags = [t.strip() for t in tags_raw.split(",") if t.strip()]

    print()
    post_text = collect_post_text()

    if not post_text:
        sys.exit("No post text entered — exiting.")

    print()
    why = prompt("Why did you save this? (1-2 sentences on the insight/framework)")

    # Build filename from first 8 words of post text
    first_words = " ".join(post_text.split()[:8])
    filename = f"{post_date}-{slugify(first_words)}.md"

    author_dir = OUTPUT_DIR / slug
    author_dir.mkdir(parents=True, exist_ok=True)
    filepath = author_dir / filename

    tags_yaml = "[" + ", ".join(tags) + "]"

    content = f"""---
author: {display_name}
author_slug: {slug}
date: {post_date}
url: {url}
likes: ~{likes}
topic_tags: {tags_yaml}
---

{post_text}

---

**Why I saved this:**
{why}
"""

    filepath.write_text(content, encoding="utf-8")
    print(f"\n  ✓ Saved → {filepath.relative_to(REPO_ROOT)}")
    print()


if __name__ == "__main__":
    main()
