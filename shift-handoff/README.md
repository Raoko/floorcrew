# ShiftHandoff

> Dump your messy shift notes. Get back a clean, structured handoff brief for the next tech — in 10 seconds.

---

## The Problem

At shift change, critical context evaporates.

The outgoing tech knows which nodes are acting up, which tickets are half-resolved, which things need eyes on, and which cages to avoid touching until a part arrives. That knowledge lives in their head. When they walk out the door, it's gone.

The incoming tech starts cold. They open the ticket queue, see a wall of open items, and have no way to know what's urgent, what's waiting, and what somebody is already handling. The result:

- Duplicated work (two techs start on the same node in different shifts)
- Missed follow-ups (critical item buried in an unread ticket)
- Tickets that bounce between shifts for days without resolution
- Incidents that could have been caught if the incoming tech had known to watch for them

---

## The Solution

**ShiftHandoff** takes messy, end-of-shift notes in any format and turns them into a clean, structured handoff brief in seconds.

Input:
```
gpu12 still janky after reboot, waiting on cage swap from warehouse
r04 u08 thermal - checked paste, better but watch it
ticket 44821 blocked on infra team, dont close
new rack in row 7 powered on but havent run burn-in yet
```

Output:
```
SHIFT HANDOFF BRIEF — March 9, 2026 · Romeo Patino → Incoming Tech

OPEN ITEMS
─────────────────────────────────────────────────
[ ] GPU-R12-U?? — Thermal/instability after reboot
    Status: Waiting on cage swap from warehouse
    Action: Do not mark resolved until part arrives

[ ] GPU-R04-U08 — Thermal throttling
    Status: Thermal paste reapplied, improved
    Action: Monitor — flag if temps spike again

[ ] Ticket #44821 — Blocked: waiting on Infra team
    Action: Do not close. Follow up with Infra EOD.

WATCH LIST
─────────────────────────────────────────────────
⚠  GPU-R04-U08 — Thermal — check at start of shift
⚠  Row 7 new rack — burn-in not yet run

FIRST ACTIONS FOR INCOMING SHIFT
─────────────────────────────────────────────────
1. Check GPU-R04-U08 temps before anything else
2. Ping warehouse on cage swap ETA for GPU-R12
3. Run burn-in on Row 7 rack if time allows
```

---

## Demo Scenarios

### Scenario 1 — Standard Shift Change
Outgoing tech pastes 6 lines of notes. Tool generates a full structured brief in under 10 seconds. Side-by-side before/after on screen.

### Scenario 2 — Messy Input, Clean Output
Input is abbreviations, slang, and shorthand ("dont touch r04", "44821 still stuck", "warehouse slow"). Claude normalizes it into professional, routable output.

### Scenario 3 — Watch List Highlight
Notes mention a node that "seemed fine but was acting weird." Tool categorizes it as WATCH rather than closed, prompts incoming tech to verify at shift start.

---

## Why This Exists

This problem is not unique to CoreWeave. Every shift-based operations team — data centers, hospitals, factories, call centers — has some version of this. But the DC floor version is particularly high-stakes: the systems being handed off affect live workloads, and the documentation gap is especially wide because techs are moving fast in physical space.

The AI angle is straightforward and believable: Claude normalizes free-form text into structured output. That's not a stretch — it's one of the most proven use cases for LLMs.

---

## How to Run

```bash
# Requires ANTHROPIC_API_KEY in environment

cd ~/hackathon/shift-handoff
python cli.py "your shift notes here"

# Or use the web form
open index.html
```

---

## Build Order

| Step | File | Est. Time |
|------|------|-----------|
| 1 | `examples/` — 3 sample inputs + expected outputs | 20 min |
| 2 | `handoff.py` — Claude prompt + output parser | 30 min |
| 3 | `cli.py` — stdin → brief → stdout | 15 min |
| 4 | `index.html` — textarea input + formatted output | 40 min |
| **Total** | | **~1.75 hours** |

---

## Pitch Lines

> "The outgoing tech knew everything. The incoming tech knew nothing. This closes that gap."

> "The input is messy. The output is professional. The AI does the translation."

> "Your Slack messages and ticket notes already contain the handoff. We just extract it."

---

## Honest Assessment

**Best use case:** DC ops teams with consistent shift rotations and no formal handoff tooling.

**Biggest risk:** This problem space has a lot of "AI summarization" tools in it. The winning angle is specificity — positioning this as a DC-floor handoff tool, not a generic meeting summarizer. The demo must feature real-sounding DC content (rack IDs, ticket numbers, part names) to feel authentic.

---

## What's Next

- Slack integration — bot listens for shift-change messages, auto-formats them
- Jira/ServiceNow write-back — handoff items become follow-up tasks automatically
- Shift history — track which items got handed off vs. resolved within-shift

---

## Track

💻 **Productivity at Scale** — 10x faster workflows across the company

**Win probability estimate: 65%**

---

*CoreWeave Hackathon 2026 — More. Better. Faster.*
