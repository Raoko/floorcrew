# Hackathon Research & Idea Development
_Compiled from ChatGPT + Glean conversations_

---

## TL;DR — What We Landed On

**🔥 Chosen Project: FBS–DSR Cable Pull Impact Visualizer**

> "When someone is about to unplug an FBS uplink to a DSR in EVI01, this tool shows exactly what they're risking: which fabric switches, which backbone paths, and what level of impact they're taking on."

---

## Key Mental Shift (The Most Important Insight)

> **Original ≠ Executive-level fantasy system**
> **Original = narrow, real, owned, and shippable in 48 hours**

Winning hackathon projects in 2026:
- Close the loop (detect → decide → act → verify)
- Touch the physical world (racks, power, cooling, IB topology, real DC workflows)
- Have a clear owner post-hackathon
- Are narrow but deep
- Are quantifiable

---

## Ideas We Rejected (and Why)

### Dead on arrival
- Internal LLM chatbot ("ChatGPT for CoreWeave") — 5+ teams will build this
- GPU utilization dashboard — "yet another dashboard"
- Log summarizer — 2023 content, every vendor demos this
- Internal AI copilot — competing with GitHub Copilot, Cursor
- "Single pane of glass" dashboard — buzzword fatigue
- Alert noise reduction — no one trusts it without proven data
- Generic agent framework — too meta and hand-wavy

### Only works with sharp execution
- AI incident triage — needs one specific incident type + proven time reduction
- Cost optimization recommender — needs real integration, not just "you could save $X"
- Capacity forecasting — needs fresh dimension (IB fabric, power/cooling limits)
- Revenue-at-risk heatmap — requires finance data access you probably don't have
- Executive lie detector — politically dangerous

### Good but too software-only
- Blast radius preview for tickets (our v1 idea)
- Ticket stall buster
- Repeat offender finder
- Walking distance optimizer
- GPU fragmentation micro-scope

---

## Physical Direction (Where We Pivoted)

Almost everyone at an AI infra hackathon will stay in software/AI-land.

Physical ideas that stand out:
- Touch racks, power, airflow, cables, movement, physical constraints
- Combine a physical signal + a small brain + a decision output + a visual moment

### Strong physical candidates we explored
| # | Idea | Why Strong |
|---|------|-----------|
| 22 | Single Point of Failure Hunter | Reveals hidden redundancy illusions, no sensors needed |
| 23 | Maintenance Risk Simulator | Scenario modeling for "what if redundancy already degraded" |
| 24 | Power Phase Guardrail | Prevents human error during installs |
| **25** | **Cable Pull Impact Visualizer** | **Hyper-realistic, high-risk activity, demoable, DC-native** |
| 26 | Thermal Drift Canary (software sim) | Physical story, no hardware risk |

---

## 🔥 The Winning Idea: Cable Pull Impact Visualizer

### Why almost nobody else will build this
- Requires knowing cable naming patterns
- Requires knowing how DSR ↔ DWDM ↔ FBS relationships work
- Requires knowing what actually scares people during maintenance
- Software engineers don't live at this layer — you do

### Why it's judge-friendly
- Concrete
- High-risk activity it addresses
- Preventative (not reactive)
- Not a dashboard, not a toy, not an LLM wrapper
- Not political

### The demo writes itself
> "Imagine we're about to reseat Vinakom port c33 on DSR1…"
> Click. Red zone lights up.
> "Removing this reduces backbone capacity 50% unless DSR2 + DWDM path B confirmed healthy."

### Chosen slice: FBS ↔ DSR uplinks
- FBS switches (SN5610) in FCR racks connect GPU fabric to backbone routers
- Their uplinks carry huge GPU traffic
- Often wired in redundant patterns that look safe but share hidden common points
- High consequence if pulled incorrectly

---

## Project Spec

### Problem
When a DCT is about to reseat an optic, swap a cable, or move an uplink on an FBS→DSR connection, it's hard to quickly answer: **"If I pull this cable right now, what's the blast radius?"**

### What it does
Given a cable ID (e.g., `FBS01_UP_A`):
1. Looks up from/to device, port, zone, rack
2. Finds the redundancy group (all uplinks protecting the same FBS)
3. Computes: "how many healthy uplinks remain after this pull?"
4. Outputs:
   - Risk level (LOW / MEDIUM / HIGH)
   - Impact description
   - Suggested checks before pulling
   - Ready-to-paste MAINT/Jira note
5. Supports "scenario mode": mark other cables as already down, then simulate

### Scope (48-hour)
**In scope:**
- Site: EVI01 only
- Domain: FBS → DSR uplinks only
- Static topology (JSON files, no live integration)
- CLI + optional web UI

**Out of scope:**
- Live Jira/Slack integration
- Multi-site
- Real-time telemetry
- Complex graph database

### Risk levels
| Scenario | Level |
|----------|-------|
| Single-uplink group, pulling it | HIGH |
| 2+ uplinks, 1 already down, pulling the other | HIGH |
| 2+ uplinks, all healthy, pulling one | MEDIUM |
| 3+ uplinks, 2+ remain after pull | LOW |

---

## File Structure

```
fbs_dsr_cable_impact/
  devices.json       # FBS + DSR metadata (rack, zone, role)
  cables.json        # Cable registry with redundancy groups
  impact.py          # Core logic: lookup + risk compute + output dict
  cli.py             # CLI: python cli.py FBS01_UP_A [--down FBS01_UP_B]
  app.py             # Optional: Flask web UI
  templates/
    index.html       # Cable picker + "mark down" checkboxes + risk card
```

---

## 48-Hour Plan

### Day 1 — Morning: Data modeling
- Pick 2-4 FBS switches and their uplinks (FBS-01, FBS-02, one single-uplink FBS)
- Build `devices.json` (FBS + DSR devices: name, rack, zone)
- Build `cables.json` (4-8 cables: IDs, from/to, redundancy_group, lag_group)

### Day 1 — Afternoon: Core logic
- `load_devices()`, `load_cables()`
- `get_cable(cable_id)`
- `cables_in_group(group)` 
- `compute_risk_for_pull(cable, marked_down=set())`
- CLI: `python cli.py FBS01_UP_A`

### Day 2 — Morning: Web UI + state
- "Marked down" list (scenario modeling)
- Flask app with cable dropdown + risk card display
- Chain scenarios: mark FBS01_UP_B down → simulate FBS01_UP_A pull → HIGH

### Day 2 — Afternoon: Demo story + slides
**3 pre-canned scenarios:**
1. Both uplinks up → pull one → MEDIUM (2→1)
2. One already marked down → pull other → HIGH (1→0)
3. Single-uplink FBS → any pull → HIGH

**4-slide deck:**
1. Problem: FBS uplink work is scary and manual
2. Idea: FBS–DSR Cable Pull Impact Visualizer
3. Demo: 2→1 uplink, then 1→0 uplink
4. Future: integrate with MAINT + live link state

---

## Judging Narrative

Key phrases to use when pitching:
- *"We focused on one of the scariest real-world actions DCTs take: touching FBS uplinks to DSRs at EVI01."*
- *"Today, deciding if pulling a cable is safe is tribal knowledge + guesswork."*
- *"Our tool makes that decision legible and repeatable."*
- *"This is not another AI copilot or pretty dashboard — it's a pre-failure guardrail for real physical work on the floor."*

Strategic framing: position as **first step toward automated maintenance risk modeling** and **pre-flight check for physical change events**.

---

## Implementation Notes (from ChatGPT)

### devices.json schema
```json
{
  "name": "fbs-01",
  "role": "FBS",
  "rack": "dh1:023:23",
  "zone": "Fabric Core Row (FCR)",
  "notes": "..."
}
```

### cables.json schema
```json
{
  "cable_id": "FBS01_UP_A",
  "from_device": "fbs-01",
  "from_port": "1/1",
  "to_device": "dsr1-us-central-07a",
  "to_port": "1/1/c25",
  "tier": "fabric_uplink",
  "redundancy_group": "FBS01_UPLINKS",
  "lag_group": "FBS01_LAG",
  "path_name": "GPU-Fabric-Uplink-A"
}
```

### CLI usage
```bash
python cli.py FBS01_UP_A
python cli.py FBS01_UP_A --down FBS01_UP_B
python cli.py --fbs fbs-01 --port 1/1
```

### Safety disclaimer (always show this)
> "Planning tool using static topology. Assumes all links are healthy unless marked down here. Always verify live status and follow MAINT/change process before touching production."

---

## Glean's Core Principles (Save These)

1. **Specificity beats generality** — "AI incident assistant" vs "EVPN flap auto-mitigator for DC3 Hall B" — same domain, completely different impact
2. **Closed loop > visualization** — detect → decide → act → verify
3. **Physical world beats software toys** — racks, power, cooling, IB topology
4. **Real owner beats interesting idea** — someone must care post-hackathon
5. **Measurable delta beats vibes** — even "saves 2 minutes per ticket × 50 tickets/month" is a story
6. **Authenticity > flash** — build what only you would think to build
