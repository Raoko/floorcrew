# Idea Validator

Research agent that checks if a hackathon idea already exists.

Searches GitHub, Reddit, Twitter/X, and Hacker News in parallel — then synthesizes a landscape report with maturity signals and gap analysis.

## Setup

```bash
cd hackathon/idea-validator
pip install -r requirements.txt
cp .env.example .env
# fill in API keys in .env
```

## Usage

```bash
python main.py "a tool that tracks cable pull risk in data centers"
```

Or interactive mode:

```bash
python main.py
# prompts for idea input
```

## Output

```
IDEA VALIDATOR — Landscape Report
==================================
Idea: cable pull risk tracker for data center ops

Keywords extracted: cable management, data center infrastructure, pull risk, DC ops tooling

GITHUB (4 repos found)
  - dc-cable-manager (stars: 12, last commit: 2021) — abandoned
  - infra-cable-viz (stars: 3, last commit: 2019) — abandoned

HACKER NEWS (2 posts)
  - "Anyone built tooling for cable management?" (2022, 47 pts)

REDDIT / TWITTER (via Grok)
  - r/datacenter: scattered complaints, no dedicated tool found

SYNTHESIS
  Verdict: Niche gap — tools exist but all abandoned pre-2022
  Maturity: Prototype / abandoned
  Your angle: Active maintenance + physical floor context = differentiation
  Gap: No tool accounts for live DSR load during pull scheduling
```

## API Keys

| Key | Where to get it |
|-----|----------------|
| `ANTHROPIC_API_KEY` | console.anthropic.com |
| `XAI_API_KEY` | console.x.ai |
| `GITHUB_TOKEN` | github.com/settings/tokens (optional but recommended) |
