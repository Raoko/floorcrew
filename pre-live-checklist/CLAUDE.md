# pre-live-checklist

## One-Line
Rack go-live enforcer — tech steps through a mandatory checklist before any rack powers up, with skip-blocking and optional photo confirmation.

## Problem
Racks go live with steps missed. Cable checks skipped. Labels not applied. Grounding not verified. The institutional knowledge of "what must be done before go-live" lives in people's heads and informal checklists that get ignored under time pressure. When something goes wrong post-live, it's impossible to know which step was skipped.

## What It Does
1. Tech opens checklist for a rack ID (e.g. `RACK-EVI01-R14`)
2. Steps are displayed in order — each must be explicitly confirmed before proceeding
3. Critical steps can require a photo upload as proof
4. Skipping is blocked — tech must mark a reason if bypassing a step
5. On completion: generates a timestamped sign-off log

## Demo Story
- Scenario 1: "Normal go-live — all steps green, photo on cable check, log generated"
- Scenario 2: "Tech tries to skip grounding check — blocked, must enter reason"
- Scenario 3: "Show the audit log: who checked what, when, what was skipped and why"

## Tech Stack
- Language: HTML/JS (fully client-side) or Python + HTML
- Data source: Static checklist config JSON per rack type
- UI: Web app — step-by-step wizard with progress bar

## File Structure
```
pre-live-checklist/
├── CLAUDE.md
├── README.md
├── data/
│   └── checklists.json    # Checklist templates per rack type
├── index.html             # Main checklist UI
├── app.js                 # Step logic, skip blocking, photo handling
└── logs/
    └── .gitkeep           # Where sign-off logs would be saved
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
