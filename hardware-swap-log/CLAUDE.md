# hardware-swap-log

## One-Line
Quick-capture tool for hardware swaps — voice or form input logs what was replaced, where, when, and by whom into a structured record.

## Problem
Hardware swaps go undocumented. A tech replaces a GPU at 2am, notes it in a Slack message that gets buried, and three weeks later nobody knows why that node has a different part number than the others. RMA reconciliation is manual. Asset tracking drifts. The data to understand hardware failure rates exists — it just never gets captured consistently.

## What It Does
1. Tech opens the tool after a swap
2. Fills a fast form (or speaks into a mic): node ID, slot, part removed, part installed, reason
3. Log entry is created: timestamped, structured, searchable
4. Optional: flags if the replaced part should trigger an RMA

## Demo Story
- Scenario 1: "GPU swap at end of shift — 30-second log entry, part number recorded, RMA flag auto-suggested"
- Scenario 2: "Show the swap history for a node — 4 parts replaced in 6 weeks, pattern visible"
- Scenario 3: "Export — 'here's every GPU we've swapped this month, by rack'"

## Tech Stack
- Language: HTML/JS (client-side) or Python + SQLite
- Data source: Browser localStorage or SQLite file
- UI: Simple form + history table

## File Structure
```
hardware-swap-log/
├── CLAUDE.md
├── README.md
├── index.html        # Swap entry form + history view
├── app.js            # Log logic, localStorage persistence
└── data/
    └── swaps.json    # Seed data with realistic swap history
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
