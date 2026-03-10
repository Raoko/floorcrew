# Glean's Notes — Additional Analysis
_Supplementary to RESEARCH.md_

---

## On ChatGPT's Theme Prediction ("Autonomous AI Infrastructure")

**Glean's verdict:** Directionally right about tech, but too eng-heavy and underweights cross-functional angles.

**What's realistic:**
- 3 big tracks is more likely than 7–8 taglines
- "AI-Driven Productivity" + "Customer-Obsessed AI Platform" + "Autonomous Infrastructure/Economics" is closer to real CW framing
- Past CW hackathons were always cross-functional (People, Finance, DC Ops, Sales, onboarding) — not just infra/ML/SRE
- "Agents on the GPU Cloud" and "AI Builds AI" are believable sub-themes, not the headline

---

## Glean's Ruthless Pass on Predictable Ideas

### Hard No
| Idea | Why Dead |
|------|----------|
| Internal LLM Chatbot | "hello-world of internal AI" — competing against prod efforts |
| GPU Dashboard 2.0 | "intern project" unless it actually takes actions |
| Log Summarizer | 2023 content, every vendor demos this |
| Internal AI Copilot (generic) | competing against Copilot, Cursor, years of training |
| Terraform/K8s generators | "cookie-cutter platform eng toy" |
| Alert Noise Reduction | no one trusts it without rock-solid data |
| Multi-cloud Cost Comparator | "SaaS sales slide," data quality impossible in 2 days |
| "Single Pane of Glass" | phrase alone is a red flag |
| ESG Dashboards | "nice to demo, never used" without driving real decisions |
| Self-Driving Cloud (buzzword) | marketing slide unless you truly close the loop |

### Only Works With Sharp Execution
- AI Incident Triage — needs ONE specific incident type + proven reduction
- Cost Optimizer — needs real integrations (Jira, approval flows, API changes)
- Capacity Forecasting — needs fresh dimension (IB fabric constraints, power/cooling)
- Agent Framework — too meta; pick ONE concrete agent to make it work

### Still Has Legs
- Autoscaling, node failure prediction, GPU memory fragmentation, power/cooling/lifecycle
- Enterprise Security Audit (deep on GPU/LLM infra-specific risk)
- Business leverage tools (if you have even one real dataset)

---

## Glean's Take on the Cable Pull Visualizer

**What's great:**
- Hyper-real risk: "before I break it" vs "after it broke"
- DCT-native knowledge required (cables, redundancy, paths)
- Scope-able to a believable slice

**Real weaknesses:**
1. **Data quality** — cable DBs are often incomplete/outdated; you'll hand-curate 10-20 cables for demo (fine, but be honest it's a slice)
2. **Oversimplifying redundancy** — LAG behavior, shared patch panels, already-degraded paths can create false sense of safety. Frame as: "assumes all other links are healthy"
3. **Narrowness** — sell it as a PATTERN ("this works for FBS uplinks, DWDM links, backbone circuits") not a single port
4. **Overlap with existing blast-radius work** — position clearly: "incident blast radius = after the break; this = before the pull"
5. **Risk of becoming a diagram viewer** — must have opinionated risk score + concrete guardrails + MAINT snippet

**How to fix:**
- Explicit assumption statement in UI: *"Assumes all other links are healthy unless marked down"*
- Keep data hand-modeled but believable (4–8 FBS cables)
- Generate MAINT/Jira snippet automatically (this is the "action" that prevents it from being a diagram)
- Position as: "The DCT floor companion to incident blast radius — for planned work, not post-incident"

---

## Full FBS-DSR Spec (Glean's Version)

Same as ChatGPT's spec — see `RESEARCH.md` for full implementation details.

Key additions from Glean:
- Be explicit: "We modeled FBS-01/02 for this hackathon; the pattern extends to DWDM links, backbone circuits, etc."
- The "scenario mode" (mark cable as already down, then simulate pull) is the killer demo feature — shows 2→1→0 uplinks clearly
- Judging narrative: *"This is not another AI copilot or pretty dashboard — it's a pre-failure guardrail for real physical work on the floor."*

---

## 3 Pre-Canned Demo Scenarios (Practice These)

1. **Normal** — both uplinks up → simulate pulling one → MEDIUM (2→1, redundancy lost but traffic stays)
2. **Already degraded** — mark FBS01_UP_B as down → simulate pulling FBS01_UP_A → HIGH (1→0, FBS isolated)
3. **Single-uplink device** — FBS with only one uplink defined → any pull → HIGH (no redundancy possible)

These three scenarios tell a complete story in under 3 minutes.
