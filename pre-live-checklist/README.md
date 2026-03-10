# Pre-Live Checklist

> Enforced rack go-live verification. Every step confirmed. Nothing skipped without a reason. Full audit trail.

---

## The Problem

Racks go live with steps missed.

There is institutional knowledge — specific, hard-won knowledge — about what must be verified before a rack powers up and goes into production. Cable check. Grounding. Label verification. Power path confirmation. Burn-in run. Some of this is documented in runbooks. Some of it lives in senior techs' heads. None of it is enforced.

Under time pressure, steps get skipped. Nobody catches it because there's no mechanism to catch it. The rack goes live. Six weeks later, a mysterious intermittent failure turns out to be an unseated cable that would have been caught by a 30-second check on go-live day.

When something goes wrong post-live, there's no record of what was verified and what wasn't. The investigation has to start from zero.

---

## The Solution

**Pre-Live Checklist** is a step-by-step go-live verification tool for rack deployments. It enforces completion, blocks skipping on critical steps, optionally requires photo evidence, and generates a timestamped sign-off log.

Key behaviors:
- **Ordered steps** — must be completed in sequence
- **Skip blocking** — critical steps cannot be skipped without entering a documented reason
- **Photo confirmation** — high-risk steps prompt for a photo upload as evidence
- **Sign-off log** — on completion, generates a record: who verified what, when, what was skipped and why
- **Rack-type templates** — checklist varies by rack type (GPU, storage, networking)

---

## Checklist Example — GPU Rack Go-Live

```
RACK-EVI01-R14 · GPU Rack · Go-Live Checklist
Tech: R. Patino · Started: 2026-03-09 14:22

[✓] 1. Power path confirmed — both PDUs, all breakers verified
[✓] 2. Cable run complete — all GPU power, all data cables seated
[✓] 3. Cable labels applied — rack ID on each cable, both ends
[✓] 4. Grounding verified — rack ground strap installed and torqued
[!] 5. Thermal check — intake/exhaust temps within spec
    SKIPPED — Reason: "Thermal sensors offline, monitoring team aware, ticket #44902"
[✓] 6. Burn-in initiated — memtest + GPU stress running
[✓] 7. Out-of-band access confirmed — IPMI/BMC responsive on all nodes
[ ] 8. Handoff to NOC — notify on-call of new rack in production

Completion: 7/8 steps (1 skipped with documentation)
Sign-off: R. Patino · 2026-03-09 15:07
```

---

## Demo Scenarios

### Scenario 1 — Clean Go-Live
Tech works through all 8 steps. Each confirmed with a tap. Photo taken on cable check step. Log generated on completion. "This rack is verified."

### Scenario 2 — Skip Attempt Blocked
Tech tries to tap "skip" on the grounding step. UI blocks it: "This step cannot be skipped without a documented reason." Tech enters reason. Step marked skipped-with-reason in the log.

### Scenario 3 — Audit Trail Review
Switch to log view. Show a past rack's sign-off: who verified each step, timestamps, what was skipped and why. "If something goes wrong with this rack, we know exactly what was checked."

---

## How to Run

```bash
# Fully client-side — no server needed
open ~/hackathon/pre-live-checklist/index.html
```

---

## Data Model

```json
// data/checklists.json — GPU rack template
{
  "rack_type": "gpu",
  "name": "GPU Rack Go-Live",
  "steps": [
    {
      "id": 1,
      "title": "Power path confirmed",
      "description": "Both PDUs energized, all breakers in correct state",
      "critical": true,
      "requires_photo": false
    },
    {
      "id": 2,
      "title": "Cable run complete",
      "description": "All GPU power connectors seated, all data cables dressed",
      "critical": true,
      "requires_photo": true
    }
  ]
}
```

---

## Build Order

| Step | File | Est. Time |
|------|------|-----------|
| 1 | `data/checklists.json` — 2 rack types, 8 steps each | 20 min |
| 2 | `index.html` — step-by-step wizard layout | 30 min |
| 3 | `app.js` — step logic, skip blocking, photo handler | 45 min |
| 4 | Log generation + display view | 25 min |
| **Total** | | **~2 hours** |

---

## Pitch Lines

> "The knowledge of what must be checked before go-live exists. This makes it impossible to ignore."

> "No more 'I thought someone else did the grounding check.'"

> "The audit trail means: when something goes wrong, you know exactly what was verified on day one."

---

## Honest Assessment

**Strength:** The problem is real and the enforcement mechanism is novel. The audit trail is genuinely useful to ops managers.

**Risk:** Checklist apps are everywhere. The differentiation has to be the enforcement model (skip blocking, photo evidence, audit log) — not just "a digital checklist." If the demo shows a regular checklist with a nice UI, it loses. If it shows the skip block in action, it has a chance.

---

## What's Next

- NetBox integration — auto-populate rack ID and configuration from NetBox
- Photo storage — upload to S3, attach to rack record
- Manager dashboard — view all in-progress and completed go-live checklists

---

## Track

🏎️ **Build with Velocity** — AI to accelerate and safeguard DC construction

**Win probability estimate: 62%**

---

*CoreWeave Hackathon 2026 — More. Better. Faster.*
