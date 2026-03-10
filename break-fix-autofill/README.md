# BreakFix AutoFill

> Type a node ID and what's wrong. Get a pre-filled ticket with category, priority, and resolution steps pulled from past incidents.

---

## The Problem

Break-fix tickets are written fast and written badly.

A tech is mid-incident, under pressure, dealing with a hot node at 3am. They open a ticket. They type "GPU not responding" and hit submit. Wrong category. No component specified. No resolution steps attempted. No connection to the 4 previous tickets on this exact same node with this exact same symptom.

This creates two compounding problems:

**At resolution time:** The tech resolving the ticket is flying blind. No history. No suggested steps. No awareness that last time, the fix was reseating the PCIe riser, not replacing the GPU.

**Over time:** Ticket data becomes useless for trend analysis. You can't identify your highest-failure nodes or most common resolution paths when ticket descriptions are vague and inconsistent.

The information to fix both problems already exists in the ticket system. It just never makes it back to the tech writing the new ticket.

---

## The Solution

**BreakFix AutoFill** is a ticket pre-fill tool. Type a node ID and a symptom. The tool searches past ticket history for similar incidents and returns a pre-populated ticket form:

| Field | Source |
|-------|--------|
| **Title** | Normalized from symptom input |
| **Category** | Matched from past incident categories |
| **Priority** | Derived from incident frequency on this node |
| **Affected component** | Extracted from symptom + past matches |
| **Resolution steps** | Top 2–3 steps from most similar past resolutions |
| **Node flags** | Open RMAs, recent incident count, known-bad component alerts |

The tech reviews, edits if needed, and submits. A 60-second task becomes a 15-second task with better output.

---

## Demo Scenarios

### Scenario 1 — Known Failure Pattern
```
Input: GPU-R04-U12, thermal throttling after reboot

Suggested ticket:
Title: GPU-R04-U12 — Thermal Throttle Post-Reboot
Category: Thermal / Cooling
Priority: P2 (3 prior incidents this quarter)
Component: GPU cooling assembly
Resolution steps:
  1. Check fan seating — fan 2 has been the culprit in 2 of 3 past incidents
  2. Verify thermal paste — last applied 4 months ago
  3. Inspect airflow blockage in adjacent slots

⚠ Node flag: 3 prior thermal incidents. Escalate if not resolved in 1 work order.
```

### Scenario 2 — Known-Bad Node
```
Input: GPU-R02-U03, NIC flapping

Suggested ticket:
Title: GPU-R02-U03 — NIC Link Instability
Category: Networking / NIC
Priority: P1 (open RMA on file)
Component: NIC — slot 2
Resolution steps:
  1. Check RMA-2026-0441 status before any physical intervention
  2. Do not replace NIC until RMA part arrives

⚠ Node flag: Open RMA. Do not replace components without checking RMA first.
```

### Scenario 3 — Novel Symptom
```
Input: GPU-R08-U05, display output dropped during burn-in

Suggested ticket:
Title: GPU-R08-U05 — Display Signal Loss During Burn-In
Category: GPU / Display Output (low confidence)
Priority: P2
Component: GPU (unconfirmed)
Resolution steps:
  No exact match found. Suggested starting point:
  1. Check GPU seating
  2. Verify PCIe power connectors
  3. Swap cable to confirm signal path

⚠ Low confidence match — no identical past incident found.
```

---

## How to Run

```bash
cd ~/hackathon/break-fix-autofill
python cli.py "GPU-R04-U12" "thermal throttling after reboot"

# Web UI
open index.html
```

---

## Data Model

```json
// data/ticket_history.json — sample entry
{
  "ticket_id": "TKT-2025-3847",
  "node_id": "GPU-R04-U12",
  "date": "2025-11-14",
  "symptom": "thermal throttling after reboot",
  "category": "Thermal / Cooling",
  "component": "GPU cooling assembly — fan 2",
  "priority": "P2",
  "resolution": "Reseated fan 2. Applied fresh thermal paste. Cleared throttle within 20 min.",
  "tech": "R. Patino"
}
```

---

## Build Order

| Step | File | Est. Time |
|------|------|-----------|
| 1 | `data/ticket_history.json` — 80 entries, 15 nodes, realistic content | 30 min |
| 2 | `autofill.py` — similarity match + field population | 35 min |
| 3 | `cli.py` — node ID + symptom → formatted suggestion | 15 min |
| 4 | `index.html` — form with live suggestion panel | 45 min |
| **Total** | | **~2 hours** |

---

## Pitch Lines

> "The last tech who fixed this exact problem already wrote the answer. We just pull it forward."

> "Bad tickets are a data problem. This fixes them at the source."

> "The tech at 3am shouldn't have to remember what the fix was last time. The system should tell them."

---

## Honest Assessment

**Strength:** The value is undeniable and immediate — better tickets, faster resolution, preserved knowledge.

**Risk:** This feels adjacent to many "AI autocomplete for forms" tools. The winning angle is the node-specific intelligence — not just suggesting a template, but pulling actual resolution patterns from *this exact node's history*. The demo must make that distinction clear.

---

## What's Next

- Jira/ServiceNow integration — read and write real tickets
- Confidence scoring on suggestions — show how many past matches informed the fill
- Pattern alerts — flag nodes that are generating tickets faster than baseline

---

## Track

🏎️ **Build with Velocity** — AI to accelerate DC operations and break-fix resolution

**Win probability estimate: 55%**

---

*CoreWeave Hackathon 2026 — More. Better. Faster.*
