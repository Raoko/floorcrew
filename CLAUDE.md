# Hackathon Root — CoreWeave 2026

## Key Info
- **Event:** March 23–25, 2026
- **Demo Day:** March 26 (2–5pm ET)
- **Sign-up deadline:** March 12, 2026 — channel: `#more-better-faster-2026`
- **Deliverable:** 2–3 min pre-recorded demo + optional slides + optional GitHub repo

## Focus Check (run at session start — one line only)

> `Session: Hackathon | Status: LOCKED — FloorCrew (SO-101 robot arm) | Sign-up: March 12`

Only expand if the user is working on something unrelated to the hackathon.
- **Primary build target: FloorCrew — TWO robots.** LOCKED IN.
  1. **SO-101 arm** (`robotics-site/`) — LeRobot + imitation learning for DC tasks.
  2. **Escort bot** (`escort-bot/`) — Pi 5 + Freenove 4WD, follows vendors on floor. Code scaffolded.
- Other concepts remain as options but FloorCrew is the committed project.
- Sign-up deadline: **March 12** — flag once per session if not signed up
- When the user shares any work context, generate a hackathon angle immediately

---

## App Registry

> **Key distinction — two types of entries:**
> - **New builds:** Built from scratch during the hackathon. No prior codebase. Live or dies in 48h.
> - **Extend existing:** An existing production tool gets a focused new feature shipped during the hackathon. The base already works — the delta is the demo.

### Extend Existing (production tools with hackathon features)

| App | Path | Status | Track | What's the hackathon angle |
|-----|------|--------|-------|---------------------------|
| cwhelper (cw-node-helper) | `~/dev/cw-node-helper/` | **Production — used daily.** Python TUI: Jira + NetBox + Grafana queue browser for DCT ops. The tool already works. Hackathon = ship one high-value new feature on top of it (e.g. AI ticket triage, shift handoff summary, IB fault auto-link) | Productivity at Scale | Add a feature that closes a loop the current tool visualizes but doesn't act on |

### New Builds (net-new, built during the hackathon)

| App | Path | Status | Track |
|-----|------|--------|-------|
| fbs-dsr-cable-impact | `hackathon/fbs-dsr-cable-impact/` | Option — not committed | Build with Velocity |
| dct-progression-tracker | `hackathon/dct-progression-tracker/` | Option — not committed | Productivity at Scale |
| idea-validator | `hackathon/idea-validator/` | Built — needs API keys + test | Build with Velocity (meta-tool) |
| floor-pulse | `hackathon/floor-pulse/` | Scaffolded — ready to build | Build with Velocity |
| floor-brief | `hackathon/floor-brief/` | Scaffolded — CLAUDE.md + README | Build with Velocity |
| shift-handoff | `hackathon/shift-handoff/` | Scaffolded — CLAUDE.md + README | Productivity at Scale |
| break-fix-autofill | `hackathon/break-fix-autofill/` | Scaffolded — CLAUDE.md + README | Build with Velocity |
| pre-live-checklist | `hackathon/pre-live-checklist/` | Scaffolded — CLAUDE.md + README | Build with Velocity |
| hardware-swap-log | `hackathon/hardware-swap-log/` | Scaffolded — CLAUDE.md + README | Build with Velocity |
| carrier-email-parser | `hackathon/carrier-email-parser/` | Scaffolded — CLAUDE.md + README | Productivity at Scale |
| optic-tracker | `hackathon/optic-tracker/` | **Spec written (v2)** — bulk pallet→box→checkout→cab tracking. Real workflow mapped. App rewrite needed. | Build with Velocity |
| rack-power-budget | `hackathon/rack-power-budget/` | Scaffolded — CLAUDE.md written | Build with Velocity |
| decom-checklist | `hackathon/decom-checklist/` | Scaffolded — CLAUDE.md written | Build with Velocity |
| **robotics-site (FloorCrew)** | `hackathon/robotics-site/` | **LOCKED IN** — SO-101 robot arm for DC floor tasks (optic seating, rack inspection, cable management). LeRobot framework + imitation learning. | Build with Velocity |
| **escort-bot (FloorCrew)** | `hackathon/escort-bot/` | **LOCKED IN** — Pi 5 person-following robot. Escorts vendors on DC floor. TFLite MobileNet SSD + gpiozero. Freenove 4WD chassis. Code scaffolded, awaiting hardware. | Build with Velocity |
| **floorcrew-app** | `hackathon/floorcrew-app/` | **Scaffolded** — Real-time dashboard: arm status, escort monitoring, rack scan logs, training controls, camera feeds. FastAPI + vanilla JS. | Build with Velocity |
| **optic-arm** | _(merged into FloorCrew)_ | Concept — robot arm auto-seats optics into switch ports via CV | Build with Velocity |
| **floor-rover** | _(not scaffolded)_ | Concept — autonomous DC aisle walkthrough robot with thermal/visual anomaly detection | Build with Velocity |
| **cable-bot** | _(merged into FloorCrew)_ | Concept — cable management arm that routes and dresses cables along rack rails | Build with Velocity |
| **rack-inspector** | _(merged into FloorCrew)_ | Concept — camera + CV scans rack face, detects missing drives/unseated cables/LED faults | Build with Velocity |

## /init — New App Setup

When the user says `/init [app-name]`, do the following:
1. Create `/Users/rpatino/hackathon/[app-name]/` directory
2. Create `/Users/rpatino/hackathon/[app-name]/CLAUDE.md` using the template below
3. Create `/Users/rpatino/hackathon/[app-name]/README.md` with problem + demo story scaffold
4. Add a row to the App Registry table in this file

### App CLAUDE.md Template

```markdown
# [App Name]

## One-Line
[What it does in one sentence]

## Problem
[The real pain point — who feels it, when, how often]

## What It Does
[Numbered list: input → steps → output]

## Demo Story
[3 pre-canned scenarios for the recording]

## Tech Stack
- Language:
- Data source:
- UI:

## File Structure
[tree of planned files]

## Status
- [ ] Data model defined
- [ ] Core logic built
- [ ] CLI working
- [ ] Web UI working
- [ ] Demo scenarios scripted
- [ ] Slides done
- [ ] Video recorded

## Judging Track
[Build with Velocity / Productivity at Scale / Win the Customer]

## Winning Criteria Check
- [ ] Closes a loop (not just visualizes)
- [ ] Physical/DC-native angle
- [ ] Shippable in 48h with static data
- [ ] Clear before/after story
- [ ] No finance data or politics needed
```

## Judging Tracks
1. **Build with Velocity** — AI to accelerate dev or DC construction
2. **Productivity at Scale** — 10x faster workflows (onboarding, comms, docs)
3. **Win the Customer** — speed to production for customers

## Bonus Categories
- People's Choice
- Cross Functional Team
- Most Company OKRs

## Winning Formula (from research)
- Specificity beats generality
- Closed loop > visualization
- Physical world beats software toys
- Measurable delta beats vibes
- Authenticity > flash
