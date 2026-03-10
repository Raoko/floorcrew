# Floor Pulse

> Real-time ambient awareness for DC techs. Tap when you complete a task. Watch the floor come alive.

## The Problem

DCT technicians work in a massive facility with no shared visual sense of what the team is doing. Radio is interrupt-driven. Slack is text. There's no layer that says: *the floor is busy right now, people are moving, work is happening.*

## What It Does

One tap = one completed task. Your position on the floor map pulses. Everyone connected sees it.

No login. No forms. No coordination overhead. Just presence.

## Demo

Open two tabs. Tap on one. Watch the other pulse.

Then open five tabs and script a busy shift. The floor comes alive.

## Stack

- Node.js + `ws` (WebSocket server)
- Vanilla JS + HTML Canvas (no build step)
- Static floor grid JSON (no live DC data required)

## Run It

```bash
npm install
npm start
# http://localhost:3000?tech=alpha
```

Open multiple tabs with different `?tech=` names to simulate a full crew.

## Hackathon Track

**Build with Velocity** — CoreWeave More. Better. Faster. 2026
