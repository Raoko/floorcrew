# FloorBrief

> Look up any node before you touch it. Get its full story in under 10 seconds.

---

## The Problem

Every day, DCTs walk the floor and touch nodes cold. There's no fast way to answer:

- Has this node had problems before?
- Is there an open RMA on it right now?
- How long has it been since anyone worked on it?
- Was it recently powered down before a ticket even came in?
- Is this a trending failure or a one-off?

That context exists somewhere — scattered across ticketing systems, Slack threads, and people's memories. But none of it is accessible at the floor level, in the moment it's needed. The result: techs duplicate effort, miss patterns, and walk into situations blind.

---

## The Solution

**FloorBrief** is a node lookup tool built for the floor. Type a node ID. Get its full story instantly:

| Signal | What it tells you |
|--------|------------------|
| **Past incidents** | Last 5 tickets — what broke, how it was resolved |
| **RMA status** | Open or closed RMAs on this node or its components |
| **Last worked** | Days since last work order — flags nodes that haven't been touched in a while |
| **Neglect flag** | Auto-raised if node has been inactive but has trending error signals |
| **Pre-ticket signals** | Recent power-down or power-up events that haven't generated a ticket yet |

---

## Demo Scenarios

### Scenario 1 — Clean Node
```
> lookup GPU-R04-U12

Node: GPU-R04-U12
Status: CLEAR
Last worked: 3 days ago
Open RMAs: None
Recent incidents: 0 in last 30 days
Pre-ticket signals: None

→ Safe to proceed.
```

### Scenario 2 — Neglected Node
```
> lookup GPU-R11-U08

Node: GPU-R11-U08
Status: WATCH ⚠
Last worked: 47 days ago
Open RMAs: None
Recent incidents: 3 (thermal throttle x2, NIC flap x1)
Pre-ticket signals: Thermal spike logged 18h ago — no ticket opened

→ This node has a pattern. Review incident history before work.
```

### Scenario 3 — Hot Node
```
> lookup GPU-R02-U03

Node: GPU-R02-U03
Status: HOT 🔴
Last worked: 6 hours ago (R. Patino)
Open RMAs: 1 open — GPU fan assembly (RMA-2026-0441)
Recent incidents: 5 in last 14 days
Pre-ticket signals: Powered down 6h ago, not yet rebooted

→ Active RMA. Do not modify without checking RMA status first.
```

---

## Why This Wins

**Only a DCT floor worker thinks of this.** Nobody sitting at a desk building "AI infrastructure tools" has ever stood in a row at 2am wondering if the node they're about to reseat has already had a bad week. The judges who understand DC ops will immediately recognize the gap this closes. The judges who don't will feel it through the demo.

**It closes a real loop.** Before FloorBrief: blind walkthrough. After: informed walkthrough. That's a measurable before/after story.

**Static data makes it demo-proof.** Works offline, no dependencies, runs on any laptop in any demo room with bad wifi.

---

## How to Run

```bash
# CLI
cd ~/hackathon/floor-brief
python cli.py lookup GPU-R04-U12

# Web UI
open index.html
```

---

## Data Model

All data is static JSON — realistic naming conventions, real-ish node IDs and timestamps.

```
data/
├── nodes.json          # Node registry: ID, rack, type, install date
├── incidents.json      # Ticket history: node, date, symptom, resolution
├── rma.json            # RMAs: node, component, status, opened/closed date
└── power_events.json   # Power events: node, type (down/up), timestamp, ticket_id (nullable)
```

---

## Build Order

| Step | File | Est. Time |
|------|------|-----------|
| 1 | `data/nodes.json` — 20 nodes, realistic IDs | 15 min |
| 2 | `data/incidents.json` — 50 incidents across nodes | 20 min |
| 3 | `data/rma.json` — 10 RMAs, mix of open/closed | 10 min |
| 4 | `data/power_events.json` — 30 events, some without tickets | 10 min |
| 5 | `brief.py` — lookup + scoring logic | 30 min |
| 6 | `cli.py` — colored terminal output | 20 min |
| 7 | `index.html` — web form + results display | 45 min |
| **Total** | | **~2.5 hours** |

---

## Pitch Lines

> "Every DCT has walked up to a node and had no idea what its week looked like. This tool fixes that."

> "The context exists. It just doesn't exist at the floor level. FloorBrief puts it there."

> "Type a node ID. 10 seconds. You know everything you need to know before you touch it."

---

## What's Next (post-hackathon)

- Live NetBox integration — pull real node data instead of static JSON
- Jira/ServiceNow integration — live ticket history
- Slack alert: when a node hits "HOT" status, ping the on-call tech
- Mobile-first UI for phone lookups on the floor

---

## Track

🏎️ **Build with Velocity** — AI to accelerate DC construction and ops work

**Win probability estimate: 82%**

---

*CoreWeave Hackathon 2026 — More. Better. Faster.*
