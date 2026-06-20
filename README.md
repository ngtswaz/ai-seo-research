# AI-Powered SEO Content Production — Research Project

**Topic:** AI-Powered SEO Content Production for B2B SaaS
**Status:** Research phase (collecting primary sources)

---

## Why this topic

AI content has split the B2B SaaS market into two groups. One group publishes thousands of low-quality AI pages and watches rankings collapse. The other uses AI strategically — for research, briefs, drafts, and semantic optimization — and is pulling ahead of competitors who haven't changed their workflows yet. The gap between those two groups is purely operational.

This project maps exactly what the winning operators are doing differently, by going directly to the practitioners who are building and shipping these systems, not the consultants writing about them.

---

## The 10 Experts

Each expert was chosen because they have documented, recent (2025–2026) work on AI content production — not retrofitted "AI" branding on old SEO advice. See [`research/sources.md`](research/sources.md) for full annotations and specific content to pull.

| # | Expert | Role | Why They're In |
|---|--------|------|----------------|
| 1 | **Lily Ray** | Founder, Algorythmic | GEO/AEO practitioner, real client data on LLM citation impact |
| 2 | **Bernard Huang** | CEO, Clearscope | Built AI content grading platform used by Adobe, Shopify |
| 3 | **Kevin Indig** | Founder, Growth Memo | Led SEO at Shopify, G2, Atlassian — publishes real experiment data |
| 4 | **Aleyda Solis** | Founder, Orainti | Weekly "Crawling Mondays" YouTube, AI Search Optimization Roadmap |
| 5 | **Nate Matherson** | CEO, Positional | Built content optimization toolset; hosts Optimize podcast weekly |
| 6 | **Ryan Law** | Dir. Content, Ahrefs | 900k-page AI content study; built content engineering system with Claude |
| 7 | **Ross Simmonds** | CEO, Foundation | AIM Framework for AI in content teams; distribution at scale |
| 8 | **Koray Tugberk GUBUR** | Founder, Holistic SEO | Topical Authority framework; built AI agents for semantic SEO |
| 9 | **Tomasz Niezgoda** | CMO, Surfer SEO | Co-built Surfer to $15M ARR; ships real AI content workflows |
| 10 | **Eli Schwartz** | SEO Advisor | Product-led SEO; most rigorous voice on when AI content fails |

---

## Repository Structure

```
/
├── README.md
├── research/
│   ├── sources.md                          ← all 10 experts: links, annotations, content to pull
│   ├── linkedin-posts/
│   │   ├── lily-ray/
│   │   │   └── 2025-11-14-ai-overview-traffic-impact.md
│   │   ├── bernard-huang/
│   │   ├── kevin-indig/
│   │   ├── aleyda-solis/
│   │   ├── nate-matherson/
│   │   ├── ryan-law/
│   │   ├── ross-simmonds/
│   │   ├── koray-tugberk-gubur/
│   │   ├── tomasz-niezgoda/
│   │   └── eli-schwartz/
│   ├── youtube-transcripts/
│   │   └── (same per-expert structure — populated by the script)
│   └── other/
│       ├── newsletter-excerpts/            ← Growth Memo, SEOFOMO, Surfer blog
│       ├── podcast-summaries/              ← Optimize, Lenny's, Ross Simmonds Show
│       └── frameworks/                     ← AIM, Topical Authority, Product-Led SEO
└── scripts/
    ├── fetch_youtube_transcripts.py        ← Supadata API transcript collector
    ├── save_linkedin_post.py               ← interactive formatter for manual LinkedIn posts
    └── requirements.txt
```

---

## Setup

### 1. Clone the repo and install dependencies

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
pip install -r scripts/requirements.txt
```

### 2. Get a Supadata API key (free, ~2 min)

Supadata handles YouTube transcript extraction without requiring cookies or authentication tokens.

1. Go to [supadata.ai](https://supadata.ai) → sign up for a free account
2. Copy your API key from the dashboard

```bash
export SUPADATA_API_KEY="your_key_here"
```

> **Free quota:** sufficient for this project (17 videos). Supadata handles PO token authentication internally.

---

## Collecting Content

### YouTube transcripts (automated)

```bash
# Dry run first — lists videos without downloading
python scripts/fetch_youtube_transcripts.py --dry-run

# Collect all experts
python scripts/fetch_youtube_transcripts.py

# Collect one expert only
python scripts/fetch_youtube_transcripts.py --expert ryan-law
```

Valid expert slugs:
`lily-ray` · `bernard-huang` · `kevin-indig` · `aleyda-solis` · `nate-matherson` · `ryan-law` · `ross-simmonds` · `koray-tugberk-gubur` · `tomasz-niezgoda` · `eli-schwartz`

Transcripts are saved to `research/youtube-transcripts/<expert>/<video_id>_<slug>.md`.
The script skips videos that have already been collected (safe to re-run).

### LinkedIn posts (manual + helper script)

LinkedIn blocks API access, so collection is manual. For each expert:

1. Go to their LinkedIn profile → click **Activity → Posts** → filter to recent posts
2. Find posts related to: AI SEO, content production, GEO, AI tools, workflow
3. Run the saver script to format and file them consistently:

```bash
python scripts/save_linkedin_post.py
```

Or paste directly into `research/linkedin-posts/<expert>/YYYY-MM-DD-<slug>.md` using this format:

```markdown
---
author: Ryan Law
author_slug: ryan-law
date: 2025-04-12
url: https://www.linkedin.com/posts/...
likes: ~840
topic_tags: [ai-content, content-engineering, ahrefs]
---

[post text here]

---

**Why I saved this:**
Documents the exact editorial review process Ryan uses before publishing AI-assisted content at Ahrefs — quantifies the human time required.
```

### Other content (newsletters, frameworks, podcast summaries)

Save to `research/other/` in the appropriate subfolder. No fixed format required — just include source URL and date at the top.

---

## Commit Strategy

Commit regularly as you collect, not in one giant push at the end. Suggested commit cadence:

```
feat: add initial repo structure, sources, and scripts
feat: add youtube transcripts for lily-ray and ryan-law
feat: add linkedin posts for bernard-huang (5 posts)
feat: add Koray topical authority framework notes
...
```

This shows work-in-progress discipline, which is part of what gets evaluated.

---

## Progress Tracker

- [x] Expert list researched and annotated (`research/sources.md`)
- [x] YouTube transcript collection script (`scripts/fetch_youtube_transcripts.py`)
- [x] LinkedIn post collection helper (`scripts/save_linkedin_post.py`)
- [ ] YouTube transcripts collected (run script after getting API key)
- [ ] LinkedIn posts collected — 5+ per expert minimum
- [ ] Newsletter / framework excerpts added to `research/other/`
- [ ] README updated with what was actually found

---

## Sources

See [`research/sources.md`](research/sources.md) for all verified links, YouTube channel handles, specific content URLs, and curation rationale.
