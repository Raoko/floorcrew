# floor-brief

## One-Line
Look up any node before touching it — instantly see past mistakes, open RMAs, neglect flags, and pre-ticket signals.

## Problem
DCTs walk the floor blind. Before touching a node, there's no fast way to know: has this thing had issues before? Is there an open RMA on it? Has it been neglected (no tickets in weeks but trending bad)? Was it recently powered down before a ticket even came in? All of that context exists somewhere — but not at the floor level, not in under 10 seconds.

## What It Does
1. Tech types a node ID (e.g. `GPU-R04-U12`)
2. Tool returns: last 5 incidents, open RMA status, days since last work order, neglect flag, and any pre-ticket signals (recent power events)
3. Tech touches the node with full context

## Demo Story
- Scenario 1: "Normal node — no flags, last worked 3 days ago, clean RMA"
- Scenario 2: "Neglected node — 47 days since last ticket, 3 past incidents, no open RMA but trending thermal errors"
- Scenario 3: "Hot node — RMA open, powered down 6 hours ago, 2 techs touched it this week"

## Tech Stack
- Language: Python (backend) + HTML/JS (UI)
- Data source: Static JSON (mock node history, RMA table, power events)
- UI: Single-page web app or CLI with colored output

## File Structure
```
floor-brief/
├── CLAUDE.md
├── README.md
├── data/
│   ├── nodes.json         # Node metadata
│   ├── incidents.json     # Past ticket history per node
│   ├── rma.json           # Open/closed RMAs
│   └── power_events.json  # Recent power-down/up events
├── brief.py               # Core lookup logic
├── cli.py                 # CLI interface
└── index.html             # Web UI
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
