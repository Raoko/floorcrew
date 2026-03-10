# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# Floor Pulse

## One-Line
A real-time ambient awareness layer for DC techs — tap when you complete a task, watch a wave ripple across the shared floor map, see your team working live.

## Problem
DCT techs work heads-down in a massive facility with no ambient sense of what the rest of the team is doing. Radio and Slack are interrupt-driven and text-only. There's no visual layer showing collective work velocity in real time — you can't "feel" the floor the way you can in a small team.

## What It Does
1. Tech opens Floor Pulse on their phone or a shared break-room screen
2. They tap once when they complete a task (rack installed, cable pulled, ticket closed)
3. A wave radiates outward from their position on the DC floor map
4. Everyone connected sees all waves in real time
5. The floor "pulses" with collective work — ambient, no coordination required

## Demo Story
- **Scenario 1 — Solo demo:** Open two browser tabs as "Tech A" and "Tech B." Tap on one; the other sees the wave. Shows real-time connection.
- **Scenario 2 — Shift rush:** Pre-script 5 bots firing taps at intervals across the floor — the map comes alive, showing a "busy shift" story.
- **Scenario 3 — Heatmap replay:** After 10 minutes of live taps, show a replay of where work happened on the floor, row by row.

## Tech Stack
- Language: Vanilla JS (client) + Node.js (server)
- Real-time: `ws` WebSocket library (no socket.io — keep it lean)
- UI: HTML Canvas for floor map + wave animation
- Data source: Static `floor.json` — hardcoded rack grid, no live DC data needed
- No build step, no bundler

## File Structure
```
floor-pulse/
├── server.js          # WebSocket server — broadcasts tap events to all clients
├── package.json
├── public/
│   ├── index.html     # Canvas UI, tech selector, tap button
│   ├── app.js         # Canvas rendering, wave animation, WS client
│   └── floor.json     # Static floor grid: rows, racks, positions
└── CLAUDE.md
```

## Commands
```bash
npm install          # install ws dependency
npm start            # runs server.js on port 3000
# open http://localhost:3000 in multiple tabs to test collaborative feel
```

## Architecture Notes
- `server.js` is a pure broadcast hub — receives `{ techId, rackId, x, y }` events, broadcasts to all connected clients. No persistence, no auth.
- `app.js` owns all rendering. Floor grid drawn from `floor.json`. Waves are canvas circles that expand and fade with `requestAnimationFrame`.
- `floor.json` is a flat array of rack objects: `{ id, row, col, x, y, label }`. Positions are pixel coords relative to a 1200x800 canvas.
- Tech identity is set via URL param `?tech=alpha` — no login, no auth, just a name for the demo.
- Wave physics: expand radius at ~80px/s, fade opacity linearly, die at radius 300px or opacity 0.

## Status
- [ ] Data model defined (`floor.json` schema)
- [ ] Core WebSocket logic built (`server.js`)
- [ ] Wave animation working (`app.js`)
- [ ] Multi-tab collaborative test passing
- [ ] Bot simulator for demo scenario 2
- [ ] Heatmap replay for demo scenario 3
- [ ] Mobile tap UX polished
- [ ] Demo scenarios scripted
- [ ] Video recorded

## Judging Track
Build with Velocity — demonstrates real-time tooling built fast for a physical ops environment

## Winning Criteria Check
- [ ] Closes a loop (not just visualizes) — tap = acknowledgment of completed work
- [x] Physical/DC-native angle — floor map is the literal building
- [x] Shippable in 48h with static data — no live system dependencies
- [x] Clear before/after story — "you had no ambient awareness, now you do"
- [x] No finance data or politics needed
