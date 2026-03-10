# Hardware Swap Log

> Fast-capture tool for hardware replacements. 30-second log entry. Structured, searchable, permanent record.

---

## The Problem

Hardware swaps go undocumented.

A tech replaces a GPU fan assembly at 2am. They note it in a Slack message to their team. Maybe they add a comment to a ticket. The physical repair is done. The part number of what was installed? Not recorded. The part number of what was removed? Also not recorded. Whether the removed part should trigger an RMA process? Nobody checked.

Three weeks later:
- Asset tracking shows the original part number — which is no longer in the machine
- The RMA window on the failed component expires because nobody filed it
- A second failure on the same node prompts the question: "how many times has this node had its GPU worked on?" — and nobody knows

The information needed to answer these questions was available for 30 seconds, while the tech was holding both parts in their hands. That window closed. The data was never captured.

---

## The Solution

**Hardware Swap Log** is a fast-capture tool for hardware replacements. Optimized for speed — a tech should be able to log a swap in under 30 seconds, while still standing at the rack.

Input options:
- Quick form: node ID, slot, part removed, part installed, reason
- (Optional future) Voice: speak the swap, tool transcribes and structures it

Output:
- Timestamped, structured log entry
- Auto-flag: does the removed part qualify for RMA?
- Running history per node: every swap, every part, every tech

---

## What a Log Entry Looks Like

```
SWAP LOG ENTRY
──────────────────────────────────────
Date:      2026-03-09 02:14
Tech:      R. Patino
Node:      GPU-R04-U12
Slot:      GPU Bay 2
Removed:   NVIDIA H100 Fan Assembly (PN: 900-21001-0020-000)
Installed: NVIDIA H100 Fan Assembly (PN: 900-21001-0020-001) [rev B]
Reason:    Fan failure — bearing noise, thermal throttle
Ticket:    TKT-2026-4421

RMA check: Removed part PN 900-21001-0020-000 → RMA eligible
           → File RMA within 14 days
──────────────────────────────────────
```

---

## Demo Scenarios

### Scenario 1 — Standard Swap
Tech fills in the form after a GPU fan replacement. 8 fields, 30 seconds. Log entry created. RMA flag appears: "This part is RMA-eligible — file within 14 days."

### Scenario 2 — Node History View
Switch to history view for GPU-R04-U12. Show 4 swap entries over 6 weeks: 2 fan assemblies, 1 PCIe riser, 1 NIC. "This node has had 4 parts replaced in 6 weeks — that's a pattern."

### Scenario 3 — Monthly Export
Show the export view: "Every GPU fan assembly swapped this month, by rack." 7 entries, 4 different racks. "This is the data you need to identify your highest-failure component lines."

---

## How to Run

```bash
# Client-side — no server needed
open ~/hackathon/hardware-swap-log/index.html
```

---

## Data Model

```json
// data/swaps.json — sample entry
{
  "id": "SWAP-2026-0047",
  "timestamp": "2026-03-09T02:14:00",
  "tech": "R. Patino",
  "node_id": "GPU-R04-U12",
  "slot": "GPU Bay 2",
  "part_removed": {
    "description": "NVIDIA H100 Fan Assembly",
    "part_number": "900-21001-0020-000"
  },
  "part_installed": {
    "description": "NVIDIA H100 Fan Assembly Rev B",
    "part_number": "900-21001-0020-001"
  },
  "reason": "Fan failure — bearing noise, thermal throttle",
  "ticket_id": "TKT-2026-4421",
  "rma_eligible": true,
  "rma_filed": false
}
```

---

## Build Order

| Step | File | Est. Time |
|------|------|-----------|
| 1 | `data/swaps.json` — 30 seed entries, 8 nodes, realistic PNs | 20 min |
| 2 | `index.html` — swap entry form + history table | 30 min |
| 3 | `app.js` — localStorage persistence, RMA flag logic | 30 min |
| 4 | Export view + node filter | 20 min |
| **Total** | | **~1.5 hours** |

---

## Pitch Lines

> "The data was available for 30 seconds while the tech was holding both parts. This captures it."

> "Every hardware swap that goes undocumented is a pattern you'll never see."

> "RMA windows expire. Not because techs forget to file — because nobody recorded that the part was replaced."

---

## Honest Assessment

**Strength:** The problem is real, the data model is clear, and it's fast to build.

**Risk:** This is the weakest AI story of the group. The tool works without AI — it's structured data capture with a simple RMA lookup. In a hackathon that rewards AI use, this may feel like a CRUD app. If this is the chosen idea, the pitch needs to lean on the data story (patterns, RMA compliance, asset drift) rather than the AI angle.

**Best case for choosing this:** If the hackathon scoring heavily weights "closes a real operational loop" and the judges are DC ops people who've personally dealt with undocumented swaps.

---

## What's Next

- NetBox write-back — sync swap records to asset inventory
- RMA portal integration — auto-initiate RMA filing from swap log
- Anomaly detection — flag nodes with swap frequency above baseline
- Voice input — speak the swap on the floor, tool transcribes

---

## Track

🏎️ **Build with Velocity** — AI to accelerate DC operations

**Win probability estimate: 38%**

---

*CoreWeave Hackathon 2026 — More. Better. Faster.*
