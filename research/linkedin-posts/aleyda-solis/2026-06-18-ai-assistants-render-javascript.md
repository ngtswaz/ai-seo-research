---
author: Aleyda Solís
author_slug: aleyda-solis
date: 2026-06-18
url: https://www.linkedin.com/feed/update/urn:li:activity:7473307747128733697/
likes: ~345
topic_tags: [ai-content, seo, ai-search, technical-seo, javascript-rendering, llm-crawlers]
---

🤖 Do AI Assistants Actually Render Your JavaScript when Grounding? Andre Alpar Put It to Test: The result? It's not good 👇

* US AI assistants (ChatGPT, Gemini, Claude, Copilot, Perplexity, Meta AI) read raw HTML only

* Chinese assistants (DeepSeek, ERNIE, Qwen, Kimi) and Mistral render JavaScript.

Most US systems requested only the HTML. They never even pulled the script file. But two cases sit in the grey zone between "reads text" and "runs code".

The most uncomfortable lesson has nothing to do with rendering. It is about trust.

* Self-reports are unreliable. Perplexity told in chat that it "couldn't access" the page — while its own crawler had already fetched that exact page and received an HTTP 200.

* The pipeline and the answer can disagree. Grok proved a system can run your JavaScript and still answer from the raw HTML.

* When you want to know what an AI actually did with your page, trust the server log, never the chatbot's description of itself.

If your important content is injected by JavaScript — client-side frameworks, lazy-loaded sections, content behind tabs that hydrate on load — then for ChatGPT, Gemini, Claude, Perplexity and Copilot, that content effectively does not exist.

Read it all in the link in comments 👇

---

**Why I saved this:**
Directly relevant to AI SEO content production: B2B SaaS sites are often JavaScript-heavy (React/Next.js), and this shows most US AI assistants only read raw HTML when grounding — meaning JS-injected content is invisible to them. A core technical-SEO consideration for making SaaS content citable by LLMs.
