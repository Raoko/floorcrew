# Optic Tracker

## One-Line
Bulk chain-of-custody tracking for optical transceivers — from pallet delivery to per-cab installation — so every missing optic has a paper trail.

## Problem
Optics (SFPs, QSFPs) disappear between delivery and data hall. The inventory specialist verifies box counts on arrival but never opens them. DCTs check out hundreds at a time via Slack, install them across multiple cabs, and nobody logs *which cab got how many*. When a cab shows up in the data hall missing 2 optics, there's no way to trace where they went. The gap between "checked out 500" and "installed across 20 cabs" is a black hole.

**Who feels it:** Inventory specialists (accountability), DCTs (blame), ops leads (cost).
**When:** Every build cycle. Recently: a cab arrived in the data hall missing 2 optics.
**How often:** Every time optics are staged for a new build — weekly at scale.

## Real Workflow (as-is)

1. **Delivery planned** — Inventory specialist knows what's coming (qty, type, PO)
2. **Pallet arrives** — Specialist verifies total box count and total optic count (math: boxes × qty-per-box). Does NOT open boxes.
3. **DCTs need optics** — They open boxes, count contents, verify against box label
4. **Checkout** — DCT requests 200–500 optics via Slack checkout workflow. Inventory specialist approves and marks those quantities as checked out.
5. **Install** — DCTs install optics into switches inside cabs. This is where tracking disappears.
6. **Staging** — Cabs sit in pre-staging area with optics installed in switches
7. **Data hall** — Cabs move to production floor. Missing optics discovered here.

## What This App Adds (the delta)

**One new step between 5 and 6: per-cab install logging.**

After installing optics in a cab, the DCT taps the cab ID and enters the count installed. Takes ~5 seconds. Now the system can reconcile:

- Delivery: 2,000 optics across 40 boxes
- Checked out: 500 to Team A, 500 to Team B, 1000 to Team C
- Installed: 498 across cabs X/Y/Z (Team A), 500 across cabs... (Team B)
- **Unaccounted: 2 — last seen with Team A, cabs X/Y/Z**

## Data Model

### Delivery
```
{
  id,
  date,
  poNumber,           // purchase order or shipment ref
  opticType,          // QSFP28-100G, QSFP-DD-400G, etc.
  partNumber,         // MCP1600-E003E30
  totalQty,           // total optics in this delivery
  boxCount,           // number of boxes on pallet
  qtyPerBox,          // optics per box (totalQty / boxCount)
  receivedBy,         // inventory specialist name
  verifiedAt,         // timestamp of pallet verification
  status              // received | partial | complete
}
```

### Box
```
{
  id,
  deliveryId,         // links to delivery
  boxNumber,          // 1 of N
  expectedQty,        // should match delivery.qtyPerBox
  actualQty,          // filled when DCT opens and counts (null until opened)
  openedBy,           // DCT who opened it
  openedAt,           // timestamp
  status              // sealed | opened | verified | discrepancy
}
```

### Checkout
```
{
  id,
  deliveryId,         // which delivery these came from
  qty,                // number of optics checked out (200–500 typical)
  checkedOutTo,       // person or team name
  approvedBy,         // inventory specialist who approved
  slackRef,           // optional: Slack message link/ID
  timestamp,
  status              // active | fully-installed | discrepancy
}
```

### Install (THE KEY NEW RECORD)
```
{
  id,
  checkoutId,         // links to checkout
  rackId,             // rack/cab identifier (e.g. "dh1-r257-node-04-us-central-07a")
  qtyInstalled,       // how many optics went into this cab
  installedBy,        // DCT name
  timestamp,
  notes               // optional: "switch 1 full, switch 2 partial"
}
```

### Reconciliation (computed, not stored)
```
Per checkout:
  checked_out    = checkout.qty
  installed      = SUM(installs WHERE checkoutId = checkout.id)
  unaccounted    = checked_out - installed

Per delivery:
  delivered      = delivery.totalQty
  box_verified   = SUM(boxes.actualQty WHERE deliveryId)
  checked_out    = SUM(checkouts.qty WHERE deliveryId)
  installed      = SUM(installs.qtyInstalled WHERE checkout.deliveryId)
  unaccounted    = delivered - installed
```

## Screens

### 1. Dashboard (home)
- **Top stats:** Total optics in system | Checked out | Installed | Unaccounted (red if > 0)
- **Active deliveries:** Cards showing each delivery with progress bar (delivered → checked out → installed)
- **Alerts:** Any cab or checkout with discrepancy flagged prominently
- **Recent activity:** Last 10 actions across all workflows

### 2. Receive Delivery
- Form: PO#, optic type, part number, total qty, box count, received by
- Auto-calculates qty-per-box
- Creates delivery record + N box records (all sealed)

### 3. Open Boxes
- Select delivery → see box grid (sealed vs opened)
- Tap a box → enter actual count → mark verified or flag discrepancy
- Running total: expected vs actual across all opened boxes

### 4. Checkout
- Select delivery → enter qty, person/team, approver
- Shows remaining available (delivered minus already checked out)
- Optional Slack ref field

### 5. Install (per cab) — THE MONEY SCREEN
- **Big input:** Cab ID (text input, or tap from recent list)
- **Qty installed** (number input)
- **Who** (DCT name — could default to logged-in user)
- Submit → logged. Takes 5 seconds.
- Below the form: running list of installs for current checkout, with per-cab breakdown

### 6. Reconciliation
- Per-delivery view: waterfall showing delivered → box-verified → checked out → installed → unaccounted
- Per-checkout view: who checked out how many, how many installed across which cabs, delta
- Per-cab view: which cabs have optics, how many, from which checkout
- **Red flags:** Any unaccounted quantity highlighted with last-known custodian

### 7. Activity Log
- Full audit trail: every receive, open, checkout, install, flag — timestamped, attributed

## Demo Story (3 scenarios for recording)

### Scenario 1: Happy Path
- Delivery of 480 QSFP-DD-400G arrives (10 boxes × 48 each)
- Inventory specialist verifies: 10 boxes, all accounted for
- DCT Romeo opens 2 boxes, verifies 48 each
- Romeo checks out 96 optics for 2 cabs
- Installs 48 in CAB-A1-001, 48 in CAB-A1-002
- Dashboard: 96 checked out, 96 installed, **0 unaccounted** — green across the board

### Scenario 2: The Missing Optics (the real problem)
- Same delivery. DCT Carlos checks out 200 for 4 cabs.
- Installs: 48 in CAB-B1-001, 48 in CAB-B1-002, 48 in CAB-B1-003, 48 in CAB-B1-004
- Total installed: 192. Checked out: 200. **8 unaccounted.**
- Dashboard lights up red. Reconciliation shows: Carlos, checkout #3, 8 missing. Last 4 cabs listed.
- Before this tool: "we lost some optics somewhere." After: "Carlos checked out 200, installed 192 across these 4 cabs. 8 unaccounted."

### Scenario 3: Box Discrepancy
- Delivery says 10 boxes × 48 = 480. DCT opens box #7, counts 45. 3 short.
- App flags box #7 as discrepancy. Delivery total adjusts.
- Issue caught at the box level, before it becomes a mystery at the cab level.

## Tech Stack
- Language: HTML/CSS/JS (single-page app)
- Data: localStorage (demo mode with seeded scenarios)
- UI: Phone-friendly, dark theme, big touch targets for floor use
- No backend, no auth — all client-side for hackathon demo

## File Structure
```
optic-tracker/
├── CLAUDE.md         # This spec
├── README.md         # Problem + demo story
└── index.html        # Main app — all-in-one SPA
```

## Status
- [x] Data model defined (v2 — bulk/cab-based, matches real workflow)
- [x] Core logic built (v2 rewrite complete)
- [x] Receive delivery screen
- [x] Open boxes screen
- [x] Checkout screen
- [x] Install per cab screen (key feature)
- [x] Reconciliation screen (waterfall + per-checkout breakdown)
- [x] Activity log
- [x] Demo scenarios seeded (3: happy path, missing optics, box discrepancy)
- [ ] Demo video recorded
- [ ] Slides done

## Judging Track
Build with Velocity

## Winning Criteria Check
- [x] Closes a loop (tracks custody from pallet to cab, flags exact discrepancy point)
- [x] Physical/DC-native (optics, boxes, cabs — real hardware on the floor)
- [x] Shippable in 48h with static data
- [x] Clear before/after ("lost 2 optics, no idea where" → "8 unaccounted, last custodian Carlos, cabs B1-001 through B1-004")
- [x] No finance data or politics needed
- [x] Minimal time added to existing workflow (~5 sec per cab install log)
