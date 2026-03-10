# DCT Progression Tracker

## Focus Check (run at session start — one line only)

> `Session: dct-progression-tracker | Status: Concept phase — blocked until fbs-dsr-cable-impact is demo-ready`

Only expand if the user explicitly wants to work on this app despite the block.
- Do not build anything here until `fbs-dsr-cable-impact` is shippable
- If the user wants to brainstorm or spec, that's fine — flag the build block

---

## One-Line
An AI-graded skill passport for data center technicians — XP tied to real tasks and Jira communication quality, not time served.

## Problem
DCT career progression is opaque. Promotions feel arbitrary, feedback is vague, and there's no structured way to know what skills you're missing or how your work quality compares over time. Team leads have no fast way to know who can handle what task.

Who feels it: DCTs at all levels, especially those trying to grow into senior/network roles
When: Performance reviews, task assignment, onboarding new techs
How often: Ongoing — promotion cycles, daily task routing, monthly reviews

## What It Does
1. Pulls Jira ticket history (CSV export or API) for a technician
2. AI grades each ticket comment against a DCT Communication Rubric
3. Tracks XP across skill dimensions over time
4. Outputs: overall progression level, per-skill scores, specific feedback ("Your tickets lack rack IDs 60% of the time"), trend graph

## DCT Communication Rubric (AI-graded)
Each Jira comment is scored on:
- [ ] Hostname/rack ID included
- [ ] Action taken stated clearly
- [ ] Result/outcome stated
- [ ] Next step or owner named
- [ ] References linked (MAINT#, PR#, runbook)
- [ ] No ambiguity ("done" vs "replaced NIC on cw-evi01-r042-s03, node back online")
- [ ] Response time (assigned → first comment delta)

## Skill Dimensions
| Dimension | Source |
|-----------|--------|
| Communication Quality | Jira (AI-graded rubric) |
| Ticket Complexity | Jira labels/types — are assigned tickets getting harder? |
| Response Speed | Jira timestamps |
| Follow-through | Ticket closure rate, bounce-back rate |
| Physical Skills | Self-reported or manager-confirmed |
| Knowledge Signals | Terminology, runbook references, linked tickets |

## Progression Levels
```
Floor Tech → Capable DCT → Senior DCT → DC Specialist → Platform Engineer
```
Each level has concrete unlock criteria, not "2 years experience."

## Demo Story
1. Load 30 days of Jira data for one technician
2. Show ticket quality score: 62/100 — "missing rack IDs 60% of the time, avg response 4.2h"
3. Show which rubric items are consistently failing
4. "Here's what to fix to hit 80 and qualify for Senior DCT track"

Opening line: "Right now, the only way to know if you're growing as a DCT is to wait for your annual review."

## Tech Stack
- Language: Python (Jira parsing + AI grading) + HTML dashboard
- Data source: Jira CSV export (no live API needed for demo)
- AI: Claude API — grades comments against rubric, returns JSON scores
- UI: Single HTML file with score cards + trend chart

## File Structure
```
dct-progression-tracker/
  data/
    sample_tickets.csv    # Anonymized Jira export for demo
  grader.py               # Claude API call: comment → rubric score JSON
  parser.py               # Jira CSV → structured ticket list
  scorer.py               # Aggregate scores per dimension
  dashboard.html          # Single-file HTML dashboard
  README.md
```

## Status
- [ ] Define rubric (6–8 criteria) — in progress
- [ ] Get sample Jira CSV export
- [ ] Build parser.py
- [ ] Build grader.py (Claude API integration)
- [ ] Build scorer.py
- [ ] Build dashboard.html
- [ ] Demo scenarios scripted
- [ ] Slides done
- [ ] Video recorded

## Judging Track
Productivity at Scale — multiply output, improve communication quality, make career growth legible

## Winning Criteria Check
- [x] Closes a loop — feedback → improvement → re-score
- [x] Physical/DC-native — rubric is specific to DCT terminology and workflows
- [x] Shippable in 48h with static data (CSV export)
- [x] Clear before/after story — score 62 → 81 after using tool for 2 weeks
- [x] No finance data or politics needed

## Key Questions to Resolve
1. Can we pull a Jira CSV export easily? (needed for demo data)
2. Personal tool or team-facing? (demo with own data, but frame as team tool)
3. Should AI verification be real-time or batch? (batch is fine for 48h)

## Key Pitching Lines
- "Promotions today are based on vibes. This makes the criteria legible."
- "The rubric is the IP — not the LLM. Any DCT can read it and know what good looks like."
- "This is a career passport, not another dashboard."
