#!/usr/bin/env bash
set -e

GITHUB_USER="ngtswaz"
GITHUB_TOKEN="${GITHUB_TOKEN:?Set GITHUB_TOKEN env var first}"
REPO_NAME="ai-seo-research"

echo ""
echo "==== AI SEO Research — GitHub Repo Setup ===="
echo ""

# 1. Create repo
echo "[1/5] Creating GitHub repo..."
HTTP_CODE=$(curl -s -o /tmp/gh_response.json -w "%{http_code}" \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  -X POST https://api.github.com/user/repos \
  -d "{\"name\":\"$REPO_NAME\",\"description\":\"AI-powered SEO content production research\",\"private\":false,\"auto_init\":false}")

if [ "$HTTP_CODE" = "201" ]; then
  echo "    ✓ Repo created: https://github.com/$GITHUB_USER/$REPO_NAME"
elif [ "$HTTP_CODE" = "422" ]; then
  echo "    ✓ Repo already exists — continuing"
else
  echo "    ✗ Error $HTTP_CODE:"
  cat /tmp/gh_response.json
  exit 1
fi

# 2. Git init
echo "[2/5] Initialising git..."
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"
git init -q
git config user.email "jashan.jyot_bmt2029@tetr.com"
git config user.name "ngtswaz"
echo "    ✓ Git initialised in $SCRIPT_DIR"

# 3. Build folder structure
echo "[3/5] Building folder structure..."
for expert in lily-ray bernard-huang kevin-indig aleyda-solis nate-matherson ryan-law ross-simmonds koray-tugberk-gubur tomasz-niezgoda eli-schwartz; do
  mkdir -p "research/linkedin-posts/$expert"
  touch "research/linkedin-posts/$expert/.gitkeep"
  mkdir -p "research/youtube-transcripts/$expert"
  touch "research/youtube-transcripts/$expert/.gitkeep"
done
mkdir -p research/other/newsletter-excerpts research/other/podcast-summaries research/other/frameworks
touch research/other/newsletter-excerpts/.gitkeep research/other/podcast-summaries/.gitkeep research/other/frameworks/.gitkeep
mkdir -p scripts

# Move files into correct locations
[ -f "sources.md" ]                   && mv sources.md research/sources.md && echo "    Moved sources.md → research/sources.md"
[ -f "fetch_youtube_transcripts.py" ] && mv fetch_youtube_transcripts.py scripts/ && echo "    Moved fetch_youtube_transcripts.py → scripts/"
[ -f "save_linkedin_post.py" ]        && mv save_linkedin_post.py scripts/ && echo "    Moved save_linkedin_post.py → scripts/"
[ -f "requirements.txt" ]             && mv requirements.txt scripts/ && echo "    Moved requirements.txt → scripts/"
[ -f "linkedin-post-template.md" ]    && mv linkedin-post-template.md research/ && echo "    Moved linkedin-post-template.md → research/"
echo "    ✓ Structure ready"

# 4. Commit
echo "[4/5] Committing..."
git add .
git commit -q -m "feat: initial repo — expert sources, collection scripts, folder structure

- research/sources.md: 10 verified AI SEO experts with links + annotations
- scripts/fetch_youtube_transcripts.py: YouTube Data API v3 collector
- scripts/save_linkedin_post.py: interactive LinkedIn post formatter
- Full folder structure for linkedin-posts, youtube-transcripts, other"
echo "    ✓ Committed"

# 5. Push
echo "[5/5] Pushing to GitHub..."
git branch -M main
git remote remove origin 2>/dev/null || true
git remote add origin "https://$GITHUB_TOKEN@github.com/$GITHUB_USER/$REPO_NAME.git"
git push -u origin main -q
echo "    ✓ Pushed"

echo ""
echo "==== ✅ Done! ===="
echo "Repo: https://github.com/$GITHUB_USER/$REPO_NAME"
echo ""
