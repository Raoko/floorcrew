# FBS-DSR Cable Pull Impact Visualizer

## Focus Check (run at session start — one line only)

> `Session: fbs-dsr-cable-impact | Status: [current status] | Next: [top unchecked item from Status list]`

Only expand if the user is off-task or asking about something unrelated.
- Nothing is built yet — data model is the first step
- Do not start dct-progression-tracker until this app is demo-ready
- Sign-up deadline: **March 12** — flag if not done

---

## One-Line
Before pulling an FBS uplink to a DSR, instantly see risk level, remaining uplinks, and get a paste-ready MAINT snippet.

## Problem
When a DCT is about to reseat an optic, swap a cable, or move an uplink on an FBS→DSR connection, there's no fast way to answer: "If I pull this cable right now, what's the blast radius?" The answer today is tribal knowledge + guesswork.

Who feels it: DCTs and network techs at EVI01 doing physical maintenance on FCR racks
When: Every cable pull, optic reseat, or uplink swap on FBS switches
How often: Multiple times per maintenance window

## What It Does
Given a cable ID (e.g. `FBS01_UP_A`):
1. Looks up from/to device, port, zone, rack
2. Finds the redundancy group (all uplinks protecting the same FBS)
3. Computes how many healthy uplinks remain after this pull
4. Outputs: risk level (LOW/MEDIUM/HIGH), impact description, suggested checks, paste-ready MAINT/Jira note
5. Supports scenario mode: mark other cables as already down, then simulate

## Demo Story
1. Both uplinks healthy → pull one → MEDIUM (2→1 uplinks)
2. One already marked down → pull the other → HIGH (1→0 uplinks)
3. Single-uplink FBS → any pull → HIGH (immediate impact)

Opening line: "Imagine we're about to reseat Vinakom port c33 on DSR1… Click. Red zone lights up."

## Tech Stack
- Language: Python (core logic + CLI) + optional Flask
- Data source: Static JSON (devices.json, cables.json) — EVI01 topology
- UI: CLI first, then Flask web UI with cable picker + risk card

## File Structure
```
fbs-dsr-cable-impact/
  devices.json        # FBS + DSR metadata (rack, zone, role)
  cables.json         # Cable registry with redundancy groups
  impact.py           # Core logic: lookup + risk compute + output
  cli.py              # CLI: python cli.py FBS01_UP_A [--down FBS01_UP_B]
  app.py              # Flask web UI
  templates/
    index.html        # Cable picker + "mark down" checkboxes + risk card
```

## Status
- [ ] Data model defined (devices.json + cables.json schemas)
- [ ] Core logic built (impact.py)
- [ ] CLI working
- [ ] Web UI working
- [ ] Demo scenarios scripted
- [ ] Slides done (4 slides: problem, idea, demo, future)
- [ ] Video recorded

## Risk Levels
| Scenario | Level |
|----------|-------|
| Single-uplink group, pulling it | HIGH |
| 2+ uplinks, 1 already down, pulling the other | HIGH |
| 2+ uplinks, all healthy, pulling one | MEDIUM |
| 3+ uplinks, 2+ remain after pull | LOW |

## Judging Track
Build with Velocity — AI to accelerate DC construction/ops safety

## Safety Disclaimer (always show in UI)
"Planning tool using static topology. Assumes all links are healthy unless marked down here. Always verify live status and follow MAINT/change process before touching production."

## Winning Criteria Check
- [x] Closes a loop — detects risk before action, outputs ready-to-use MAINT note
- [x] Physical/DC-native — FBS racks, cable pulls, IB topology
- [x] Shippable in 48h with static data
- [x] Clear before/after story — tribal knowledge → legible risk card
- [x] No finance data or politics needed

## Key Pitching Lines
- "Only someone on the floor would build this"
- "This is not another AI copilot — it's a pre-failure guardrail for real physical work"
- "Today this decision is tribal knowledge. Our tool makes it legible and repeatable."
