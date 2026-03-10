# Rack Power Budget

## One-Line
Before racking a server, instantly know if the target PDU circuit can handle the load — go/no-go with exact headroom numbers.

## Problem
DCTs racking new hardware have no fast way to answer: "Will this server fit on this PDU without tripping a breaker?" Today: tribal knowledge, guessing, or waiting for a facilities check. Over-provisioned circuits cause outages.

Who feels it: DCTs and rack-and-stack techs at EVI01
When: Every new server intake and rack assignment
How often: Every build wave — multiple servers per day during active builds

## What It Does
1. Select or enter server model (pulls TDP from static lookup table)
2. Enter target rack + PDU/circuit
3. App shows: current load, new total after racking, available headroom, go/no-go verdict
4. Flags if racking would exceed 80% circuit capacity (standard safe threshold)
5. Suggests alternate circuits if over budget

## Demo Story
1. Rack a GPU server on a circuit at 60% → GREEN — safe, 20% headroom remaining
2. Same server on a circuit at 75% → YELLOW — over 80% threshold after racking
3. Two servers queued for same circuit → RED — would trip, suggests split across PDU-A/PDU-B

## Tech Stack
- Language: HTML/JS (single file, no backend)
- Data source: Static JSON — server TDP table, rack/PDU capacity map (EVI01 data)
- UI: Mobile-friendly form → risk card with go/no-go badge

## File Structure
```
rack-power-budget/
  index.html        # Main UI — server picker, rack selector, result card
  servers.json      # Server model TDP lookup (static)
  racks.json        # Rack/PDU capacity + current load (static/editable)
```

## Status
- [ ] Data model defined (servers.json + racks.json schemas)
- [ ] Core logic built (budget calculator)
- [ ] UI working
- [ ] Demo scenarios scripted
- [ ] Slides done
- [ ] Video recorded

## Judging Track
Build with Velocity — prevents physical infrastructure failures before they happen

## Winning Criteria Check
- [ ] Closes a loop — "can I rack this?" → go/no-go before touching hardware
- [ ] Physical/DC-native — PDUs, circuits, rack builds
- [ ] Shippable in 48h with static data
- [ ] Clear before/after story — guesswork → data-backed go/no-go
- [ ] No finance data or politics needed

## Key Pitching Lines
- "One circuit trip costs more downtime than this tool took to build"
- "Only a DCT would know the 80% threshold rule is the real constraint"
- "Static data is fine — the math is the value, not the API"
