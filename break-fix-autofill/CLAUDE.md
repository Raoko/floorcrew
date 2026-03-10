# break-fix-autofill

## One-Line
Type a node ID and symptom → get a pre-filled ticket with suggested category, priority, resolution steps, and historical patterns.

## Problem
Break-fix tickets are written fast and written badly. Techs under pressure fill in the minimum — vague descriptions, wrong categories, missing fields. This makes tickets hard to route, hard to search, and useless as historical data. The information asymmetry is real: the system has seen this failure before, but the tech writing the ticket doesn't know that.

## What It Does
1. Tech types node ID + symptom (e.g. "GPU-R04-U12, thermal throttling after reboot")
2. Tool searches mock ticket history for similar past incidents
3. Returns pre-filled ticket: suggested title, category, priority, affected component, and 2–3 resolution steps drawn from past fixes
4. Tech reviews, edits if needed, submits

## Demo Story
- Scenario 1: "GPU thermal — system suggests 'Check fan seating, verify thermal paste, inspect airflow blockage' from 4 past similar tickets"
- Scenario 2: "NIC flapping on a known-bad node — system flags: 'This node has 3 prior NIC incidents, open RMA on file'"
- Scenario 3: "Novel symptom — system returns best-guess template with low confidence flag"

## Tech Stack
- Language: Python
- Data source: Static JSON ticket history (50–100 fake but realistic entries)
- UI: CLI or HTML form with live suggestions

## File Structure
```
break-fix-autofill/
├── CLAUDE.md
├── README.md
├── data/
│   └── ticket_history.json   # Mock past tickets with node ID, symptom, resolution
├── autofill.py               # Lookup + suggestion logic
├── cli.py                    # CLI interface
└── index.html                # Web UI with form
```

## Status
- [ ] Data model defined
- [ ] Core logic built
- [ ] CLI working
- [ ] Web UI working
- [ ] Demo scenarios scripted
- [ ] Slides done
- [ ] Video recorded

## Judging Track
Build with Velocity

## Winning Criteria Check
- [ ] Closes a loop (not just visualizes)
- [ ] Physical/DC-native angle
- [ ] Shippable in 48h with static data
- [ ] Clear before/after story
- [ ] No finance data or politics needed
