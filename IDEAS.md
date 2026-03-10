# Hackathon Ideas — CoreWeave 2026

## Tracks

- **Build with Velocity** — Use AI to accelerate dev or DC construction
- **Productivity at Scale** — 10x faster workflows (onboarding, comms, docs)
- **Win the Customer** — Speed to production for customers
- **Bonus:** People's Choice · Cross Functional Team · Most Company OKRs

---

## 1. CW Helper — AI Feature Add-On
**Track:** Productivity at Scale · **Status:** Production tool — ship a new feature on top
**What:** Add an AI-powered feature to the existing cw-node-helper TUI — ticket triage, shift handoff summary, or IB fault auto-link.
**Problem:** The TUI already runs daily. Hackathon = ship one high-value feature that closes a loop the tool currently visualizes but doesn't act on.
**Stack:** Python TUI (existing) · Jira + NetBox + Grafana APIs

---

## 2. Cable Impact Checker
**Track:** Build with Velocity · **Status:** Spec written
**What:** Before pulling an FBS uplink to a DSR, see risk level, remaining uplinks, and get a paste-ready MAINT snippet.
**Problem:** DCTs doing cable pulls have no fast way to assess blast radius. Decision-making is tribal knowledge + guesswork. Happens multiple times per maintenance window.
**Stack:** Python CLI + Flask · Static JSON (devices, cables) · Web UI with cable picker + risk card

---

## 3. DCT Progression Tracker
**Track:** Productivity at Scale · **Status:** Concept phase
**What:** AI-graded skill passport — XP tied to real Jira tasks and communication quality, not time served.
**Problem:** Career progression is opaque. Promotions feel arbitrary. No structured way to know what skills are missing or how quality compares over time. Team leads can't quickly assess who can handle what.
**Stack:** Python · Jira CSV export · Claude API for grading · HTML dashboard with score cards + trends

---

## 4. Idea Validator
**Track:** Build with Velocity (meta-tool) · **Status:** Built — needs API keys
**What:** Research agent that checks if a hackathon idea already exists across Reddit, Twitter, GitHub, and Hacker News.
**Problem:** Before building, need to know: has this been done? Abandoned? Where's the gap? Manual searching is slow and scattered.
**Stack:** Python · xAI Grok API · GitHub REST · HN Algolia · Claude for synthesis · Rich terminal UI

---

## 5. Floor Pulse
**Track:** Build with Velocity · **Status:** Scaffolded
**What:** Real-time ambient awareness — tap when you complete a task, see a wave ripple across the shared floor map. Team sees each other working live.
**Problem:** Techs work heads-down in a massive facility with no ambient sense of what the rest of the team is doing. Radio and Slack are interrupt-driven, text-only. No visual layer for collective work velocity.
**Stack:** Vanilla JS + Node.js · WebSocket · HTML Canvas floor map + wave animation · Static floor grid JSON

---

## 6. Floor Brief
**Track:** Build with Velocity · **Status:** Scaffolded
**What:** Look up any node before touching it — see past incidents, open RMAs, neglect flags, and pre-ticket signals in under 10 seconds.
**Problem:** DCTs walk the floor blind. Context exists across systems but not at floor level, not fast enough. No way to know if a node has had issues, has an open RMA, or has been neglected.
**Stack:** Python + HTML/JS · Static JSON (mock node history, RMA table, power events)

---

## 7. Shift Handoff
**Track:** Productivity at Scale · **Status:** Scaffolded
**What:** Dump open tickets and floor notes, get back a structured handoff doc for the next tech. Copy-paste ready for Slack.
**Problem:** At shift change, critical context gets lost. Outgoing tech knows which nodes are flaky, which tickets are half-done — but it stays in their head. Incoming tech starts cold. Duplicated effort, missed follow-ups, bouncing tickets.
**Stack:** Python · Free-form text input · Claude API · CLI or HTML form

---

## 8. Break-Fix Autofill
**Track:** Build with Velocity · **Status:** Scaffolded
**What:** Type a node ID + symptom, get a pre-filled ticket with category, priority, resolution steps, and patterns from past fixes.
**Problem:** Break-fix tickets are written fast and badly. Vague descriptions, wrong categories, missing fields. Makes tickets hard to route and useless as historical data. The system has seen this before — the tech writing the ticket doesn't know.
**Stack:** Python · Static JSON ticket history (50–100 entries) · CLI or HTML form with live suggestions

---

## 9. Pre-Live Checklist
**Track:** Build with Velocity · **Status:** Scaffolded
**What:** Mandatory step-by-step checklist before any rack powers up. Skip-blocking, optional photo confirmation, timestamped sign-off.
**Problem:** Racks go live with steps missed — cable checks skipped, labels not applied, grounding not verified. When things go wrong post-live, impossible to trace which step was skipped.
**Stack:** HTML/JS (client-side) · Static checklist config JSON per rack type · Step wizard with progress bar

---

## 10. Hardware Swap Log
**Track:** Build with Velocity · **Status:** Scaffolded
**What:** Quick-capture tool for hardware swaps — form or voice input logs what was replaced, where, when, and by whom.
**Problem:** Swaps go undocumented. Replacement noted in Slack, gets buried. Three weeks later nobody knows why a node has a different part number. RMA reconciliation is manual. Asset tracking drifts.
**Stack:** HTML/JS or Python + SQLite · localStorage or SQLite · Simple form + history table

---

## 11. Carrier Email Parser
**Track:** Productivity at Scale · **Status:** Scaffolded — blocked on gws CLI
**What:** Auto-classify carrier maintenance emails, ID CW vs carrier responsibility, draft responses for backbone events.
**Problem:** Network Ops manually reads tons of carrier emails, cross-references CW infrastructure, decides responsibility, drafts responses. Hours per shift. Semi-structured formats vary by provider. Volume high enough things get missed.
**Stack:** Python · Static sample emails for demo (gws CLI for live, pending IT) · Claude/Gemini for classification · HTML dashboard

---

## 12. Optic Tracker
**Track:** Build with Velocity · **Status:** Spec written (v2)
**What:** Bulk chain-of-custody tracking for optics — pallet delivery to per-cab install. Every missing optic has a paper trail.
**Problem:** Optics disappear between delivery and data hall. Inventory verifies box counts but never opens them. DCTs check out hundreds, install across cabs, nobody logs which cab got how many. The gap between "checked out 500" and "installed across 20 cabs" is a black hole.
**Stack:** HTML/CSS/JS (single-page app) · localStorage with seeded scenarios · Phone-friendly, dark theme, big touch targets

---

## 13. Rack Power Budget
**Track:** Build with Velocity · **Status:** Scaffolded
**What:** Before racking a server, instantly know if the PDU circuit can handle the load — go/no-go with exact headroom.
**Problem:** DCTs have no fast way to answer "will this server fit on this PDU without tripping the breaker?" Today: tribal knowledge, guessing, or waiting for facilities. Over-provisioned circuits cause outages.
**Stack:** HTML/JS (single file) · Static JSON server TDP table + rack/PDU capacity map · Mobile form → risk card with go/no-go badge

---

## 14. Decom Checklist
**Track:** Build with Velocity · **Status:** Scaffolded
**What:** Guided decommission workflow — ordered steps with timestamps, nothing skipped, completion record at the end.
**Problem:** Decom has an ordered sequence (ticket verify → power down → cable removal → asset scan → staging) but today it's tribal knowledge and paper. Wrong serial logged, live cable pulled, ticket not updated — common and expensive.
**Stack:** HTML/JS (single file) · Static step definitions · Mobile-first · localStorage for session resume

---

## 15. Optic Arm
**Track:** Build with Velocity · **Status:** Concept only
**What:** Robot arm that auto-seats optical transceivers into switch ports using computer vision.

---

## 16. Floor Rover
**Track:** Build with Velocity · **Status:** Concept only
**What:** Autonomous DC aisle walkthrough robot with thermal and visual anomaly detection.

---

## 17. Cable Bot
**Track:** Build with Velocity · **Status:** Concept only
**What:** Cable management arm that routes and dresses cables along rack rails.

---

## 18. Rack Inspector
**Track:** Build with Velocity · **Status:** Concept only
**What:** Camera + CV scans rack face, detects missing drives, unseated cables, and LED faults.

---

## Chosen Idea: TBD
**Why this one:**
