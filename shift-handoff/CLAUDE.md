# shift-handoff

## One-Line
End-of-shift AI brief: dump your open tickets and floor notes, get back a structured handoff doc for the next tech.

## Problem
At shift change, critical context gets lost. The outgoing tech knows which nodes are acting up, which tickets are half-resolved, and which things need eyes on — but that knowledge lives in their head, not in any system. The incoming tech starts cold. This causes duplicated effort, missed follow-ups, and tickets that bounce between shifts for days.

## What It Does
1. Tech pastes or types their open tickets + any floor notes (free-form, messy is fine)
2. Claude normalizes the input and generates a structured handoff brief:
   - Open items with status
   - Watch list (nodes that need monitoring)
   - Blocked items and why
   - Recommended first actions for incoming shift
3. Output is copy-paste ready for Slack or ticket system

## Demo Story
- Scenario 1: "3 open tickets, 2 nodes on watch — incoming tech gets a clean brief in 10 seconds"
- Scenario 2: "Messy notes ('gpu12 still janky, waiting on cage swap, dont touch r04') → structured professional handoff"
- Scenario 3: "Show the before/after: raw notes vs. formatted brief side by side"

## Tech Stack
- Language: Python
- Data source: Free-form text input + Claude API
- UI: CLI or simple HTML form

## File Structure
```
shift-handoff/
├── CLAUDE.md
├── README.md
├── handoff.py       # Core Claude call + formatting
├── cli.py           # CLI interface
├── index.html       # Web form UI
└── examples/
    ├── input1.txt   # Sample messy shift notes
    └── output1.md   # Sample structured brief
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
Productivity at Scale

## Winning Criteria Check
- [ ] Closes a loop (not just visualizes)
- [ ] Physical/DC-native angle
- [ ] Shippable in 48h with static data
- [ ] Clear before/after story
- [ ] No finance data or politics needed
