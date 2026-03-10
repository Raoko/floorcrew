# Idea Validator

## One-Line
Research agent that checks if a hackathon idea already exists across Reddit, Twitter, GitHub, and Hacker News.

## Problem
Before building, you need to know: has this been done? Is it abandoned? Where's the gap?
Manual searching is slow and scattered. This agent does it in parallel and synthesizes the landscape.

## What It Does
1. Input: raw idea description (messy natural language OK)
2. Claude normalizes it → extracts search keywords
3. Parallel search: GitHub repos + Grok (Reddit/Twitter) + HN Algolia
4. Claude synthesizes results into a landscape report
5. Output: maturity signal, gap analysis, differentiation angle

## Tech Stack
- Language: Python 3.11+
- APIs: xAI Grok (web search), GitHub REST API, HN Algolia API
- AI: Claude (claude-sonnet-4-6) for keyword extraction + synthesis
- UI: Terminal (rich for formatting)

## File Structure
```
idea-validator/
├── main.py           # CLI entry + orchestration
├── search/
│   ├── __init__.py
│   ├── github.py     # GitHub repo search
│   ├── grok.py       # xAI Grok — Reddit + Twitter/X
│   └── hn.py         # Hacker News Algolia
├── synthesize.py     # Claude synthesis layer
├── .env.example
├── requirements.txt
├── CLAUDE.md
└── README.md
```

## Status
- [x] File structure created
- [x] GitHub search built
- [x] HN search built
- [x] Grok search built
- [x] Claude synthesis built
- [x] CLI working
- [ ] Tested end-to-end
- [ ] Output tuned

## Judging Track
Build with Velocity (meta-tool for hackathon ideation)

## Env Vars Required
- `ANTHROPIC_API_KEY`
- `XAI_API_KEY` — get from console.x.ai
- `GITHUB_TOKEN` — optional, raises rate limit from 10/min to 30/min
