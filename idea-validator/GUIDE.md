# Idea Validator — Detailed Guide

## What It Does

Idea Validator is a research agent that answers one question:
**Has this been built before, and if so, how mature is it?**

You paste a raw idea. It searches GitHub, Hacker News, and Reddit/Twitter (via Grok) in parallel, then uses Claude to synthesize a landscape report — verdict, maturity signal, existing players, and the gap your idea could own.

---

## How It Works (Architecture)

```
Your idea (messy natural language)
         │
         ▼
  Claude — keyword extraction
  "cable pull risk tracker for data centers"
   → ["cable management", "data center ops", "pull risk", "DC tooling"]
         │
         ├──────────────────────────────────┐──────────────────────────────────┐
         ▼                                  ▼                                  ▼
   GitHub REST API               HN Algolia API                  xAI Grok (web search)
   /search/repositories          /search?tags=story              model: grok-2-latest
   sorted by stars               top stories only                search_parameters: on
   returns: name, stars,         returns: title, pts,            prompt: search Reddit
   last push, language,          comments, date, url             and Twitter/X for
   archived flag                                                  discussions
         │                                  │                                  │
         └──────────────────────────────────┴──────────────────────────────────┘
                                            │
                                            ▼
                              Claude — synthesis (claude-sonnet-4-6)
                              Verdict + Maturity + Gap + Angle
                                            │
                                            ▼
                              Rich terminal report
```

**All three searches run in parallel** (ThreadPoolExecutor) — total wall time is the slowest single search, not the sum.

---

## Setup — Step by Step

### 1. Get your API keys

**Anthropic (Claude):**
- Go to `console.anthropic.com`
- API Keys → Create Key
- Copy it

**xAI (Grok with web search):**
- Go to `console.x.ai`
- Create account / sign in
- API Keys → Create Key
- Copy it (this is what powers the Reddit + Twitter search lane)

**GitHub token (optional but recommended):**
- Go to `github.com/settings/tokens`
- Generate new token (classic) → no scopes needed for public search
- Copy it
- Without this: 10 requests/min rate limit
- With this: 30 requests/min rate limit

### 2. Install dependencies

```bash
cd ~/hackathon/idea-validator
pip install -r requirements.txt
```

What gets installed:
- `anthropic` — Claude API client
- `openai` — used as the xAI/Grok client (xAI is OpenAI-compatible)
- `httpx` — HTTP client for GitHub and HN API calls
- `rich` — terminal formatting (panels, rules, spinners)
- `python-dotenv` — loads .env file

### 3. Configure your .env

```bash
cp .env.example .env
```

Edit `.env`:
```
ANTHROPIC_API_KEY=sk-ant-...
XAI_API_KEY=xai-...
GITHUB_TOKEN=ghp_...   # optional
```

---

## Running It

### Command line argument (fastest)

```bash
python main.py "a tool that tracks cable pull risk in data centers"
```

### Interactive mode

```bash
python main.py
# prompts: paste your idea and press Enter
```

### Any idea works — it normalizes messy input

```bash
python main.py "like a jira but for physical DC work orders that auto-prioritizes by rack temp"
python main.py "skill passport for data center techs — shows what they've proven they can do"
python main.py "something that tells you if a fiber run will conflict with active cooling zones"
```

---

## Reading the Output

### Section 1 — Keyword extraction
```
Keywords: cable management, data center infrastructure, pull scheduling, DC ops
```
Claude strips your idea down to searchable terms. If these look wrong, your idea description might be too vague — add more context.

### Section 2 — GitHub results
```
GITHUB
  torvalds/dc-tools — stars: 12 | last push: 2021-04-02 | Python
    Utilities for data center cable management
    https://github.com/torvalds/dc-tools
```

What to look for:
- **Stars < 50 + last push > 2 years ago** = abandoned, low competition
- **Stars > 500 + recent commits** = active, you're late
- **0-3 results total** = wide open or no one codes this yet
- **archived: true** = dead project, gap is real

### Section 3 — Hacker News results
```
HACKER NEWS
  Ask HN: Anyone built tooling for cable management in DCs? (2022-03, 47 pts, 31 comments)
    https://news.ycombinator.com/item?id=30123456
```

What to look for:
- High points + high comments = real demand signal
- Old post, no follow-up = problem was felt, never solved
- "Ask HN: who wants X" with no replies = weak signal

### Section 4 — Reddit / Twitter via Grok
```
REDDIT / TWITTER (via Grok)
  - r/datacenter: Multiple threads asking for cable pull scheduling tools (2021-2023)
  - No dedicated tools mentioned — people use spreadsheets
  - Twitter: 2-3 DC engineers complained about manual cable tracking in 2024
```

Grok has live web access. This is the freshest signal of the three. If Grok finds active recent discussion = problem is still unsolved and people care.

### Section 5 — Synthesis (Claude)
```
SYNTHESIS
  Verdict: Niche Gap
  Maturity: Abandoned Territory — tools exist but last touched 2021
  Key players: dc-cable-manager (12 stars, dead), infra-viz (3 stars, dead)
  Gap: No tool connects cable pull scheduling to live DSR load or rack status
  Angle: Physical-floor context + live data integration = defensible differentiation
```

**Verdicts explained:**

| Verdict | Meaning | Action |
|---------|---------|--------|
| Already Solved | Active, well-maintained tools dominate | Pivot or find a narrower angle |
| Active Competition | Multiple active projects, some traction | Build only if you have a clear differentiator |
| Niche Gap | Tools exist but old/abandoned/narrow | Strong position — move fast |
| Wide Open | Nothing found | Validate demand before building |
| Abandoned Territory | Was attempted, died | Good if the underlying pain is still real |

---

## Troubleshooting

**"XAI_API_KEY not set — skipping Grok search"**
→ Add `XAI_API_KEY` to your `.env` file. The tool still runs without it, Grok lane just shows the skip message.

**GitHub returns 403**
→ You've hit the unauthenticated rate limit (10/min). Add a `GITHUB_TOKEN` to `.env`.

**Keywords look wrong**
→ Be more specific in your idea description. Instead of "DC tool", say "data center cable pull scheduler that avoids active DSR zones."

**Grok returns generic results**
→ Your keywords may be too broad. The tool uses the keywords Claude extracted — if they're vague, Grok searches vaguely. Try a more specific idea input.

**Slow run**
→ All three searches are parallel so it should be 5-10 seconds total. If slow, Grok web search is usually the bottleneck — xAI API latency varies.

---

## File Reference

| File | Purpose |
|------|---------|
| `main.py` | CLI entry, orchestration, rich terminal output |
| `synthesize.py` | Claude calls: keyword extraction + landscape synthesis |
| `search/github.py` | GitHub REST API `/search/repositories` |
| `search/hn.py` | HN Algolia API `/search` |
| `search/grok.py` | xAI Grok with `search_parameters: on` |
| `.env` | Your API keys (never commit this) |
| `requirements.txt` | pip dependencies |

---

## Extending It

**Add Product Hunt search:**
Product Hunt has a GraphQL API. Add `search/producthunt.py` and query for posts matching your keywords. High upvotes = validated demand.

**Add npm / PyPI search:**
Check if libraries exist for your domain. `https://registry.npmjs.org/-/v1/search?text=query` and `https://pypi.org/pypi/{package}/json`.

**Save reports to file:**
Pipe output: `python main.py "your idea" > report.md`
Or add a `--save` flag to `main.py` that writes to `reports/{timestamp}.md`.

**Batch mode:**
Loop over a list of ideas from a `.txt` file — useful if you're evaluating 5-10 hackathon concepts at once.

---

## Cost Estimate

Per run (one idea):
- Claude (keyword extraction + synthesis): ~1,500 tokens → ~$0.002
- Grok web search: ~$0.01-0.02 per call (check xAI pricing)
- GitHub API: free (with token)
- HN Algolia: free

**Cost per idea validation: ~$0.02-0.03**
