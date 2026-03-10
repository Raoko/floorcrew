# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# Carrier Email Parser

## One-Line
Auto-classify carrier maintenance emails, identify CW vs carrier responsibility, and draft responses for backbone events.

## Problem
Network Ops (Thomas Scott's team) receives a TON of carrier emails about backbone maintenance, outages, and circuit issues. Today they manually:
1. Read each email to determine if it's a maintenance notice, outage alert, or action-required ticket
2. Cross-reference against CW infrastructure to determine if it affects CoreWeave
3. Decide if the issue is on CW's side or the carrier's side
4. Draft and send responses or escalate internally

This takes hours per shift. Carrier emails follow semi-structured formats but vary by provider. The volume is high enough that things get missed.

## What It Does
1. **Input:** Carrier emails (via `gws gmail` CLI or static sample data for demo)
2. **Classify:** Parse email body → categorize as: Maintenance Window / Outage / Circuit Issue / Info Only
3. **Impact Check:** Match affected circuits/sites against CW infrastructure (NetBox data or static map)
4. **Triage:** Flag as CW-action-required vs carrier-action-required vs info-only
5. **Draft Response:** Generate templated response based on classification and triage result
6. **Output:** Dashboard showing queue of parsed emails with classifications, impact, and draft responses

## Demo Story
1. **Scenario 1 — Planned Maintenance:** Carrier sends "Scheduled maintenance on circuit XYZ, March 25, 2am-4am CT." Parser classifies as Maintenance, maps to EVI01 spine uplink, flags as info-only (redundant path exists), drafts acknowledgment.
2. **Scenario 2 — Outage Alert:** Carrier sends "Unplanned outage on circuit ABC, investigating." Parser classifies as Outage, maps to critical EVI01 path, flags as CW-action-required, drafts escalation email to carrier + internal Slack alert.
3. **Scenario 3 — Carrier Needs Info:** Carrier sends "Please confirm your side of circuit DEF is clean." Parser classifies as Circuit Issue, flags as CW-action-required, drafts response with last-known interface stats.

## Tech Stack
- Language: Python
- Data source: Static sample emails (JSON/EML) for demo; `gws gmail` CLI for live mode (pending CW IT approval)
- Infrastructure data: Static JSON map of circuits → CW sites (mock NetBox export)
- AI: Claude API or Gemini for email classification + response drafting
- UI: HTML dashboard (single page) showing email queue, classifications, draft responses

## File Structure
```
carrier-email-parser/
  CLAUDE.md
  README.md
  parser.py          # Core: email parsing + classification logic
  triage.py          # Impact check against infrastructure map
  drafter.py         # Response template generation
  data/
    sample-emails/   # Static carrier email samples (JSON)
    circuits.json    # Mock circuit-to-site mapping
  dashboard/
    index.html       # Email queue + classification + draft response viewer
  config.py          # API keys, settings (gitignored)
  .gitignore
```

## Status
- [x] CLAUDE.md written
- [x] README.md scaffolded
- [ ] Data model defined (email schema, classification enum, circuit map)
- [ ] Sample emails created (3+ realistic carrier formats)
- [ ] Core parser logic built
- [ ] Triage logic built
- [ ] Response drafter built
- [ ] Web UI / dashboard working
- [ ] Demo scenarios scripted
- [ ] Slides done
- [ ] Video recorded

## Judging Track
**Productivity at Scale** — 10x faster carrier email triage for Network Ops

## Winning Criteria Check
- [x] Closes a loop (classifies AND drafts response, not just visualizes)
- [x] Physical/DC-native angle (carrier circuits map to real DC infrastructure)
- [x] Shippable in 48h with static data (sample emails + mock circuit map)
- [x] Clear before/after story (manual 15-min triage per email → instant classification + draft)
- [x] No finance data or politics needed

## Dependencies / Risks
- **`gws` CLI:** Live email access blocked pending CW IT approval (Josh Frantz proposal). Demo works with static data regardless.
- **Thomas Scott:** Natural collab partner — he already has an agent with carrier classification logic. Reach out before March 12 sign-up deadline.
- **API key:** Needs working Claude or Gemini API for classification. ANTHROPIC_API_KEY credits may be exhausted — check first.

## Collab Notes
- Thomas Scott (Network Ops) described this exact use case in `#ai-tool-usage` Slack on March 9, 2026
- He has an existing agent with "decent track rate" for CW vs carrier identification
- Cross-functional team = bonus judging category
