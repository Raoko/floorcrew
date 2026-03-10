# Optic Tracker

**Bulk chain-of-custody for optical transceivers — from pallet to cab.**

## Problem
Optics disappear between delivery and data hall. The inventory specialist verifies box counts but doesn't open them. DCTs check out hundreds via Slack and install across multiple cabs. Nobody logs which cab got how many. When a cab arrives in the data hall missing 2 optics, there's no paper trail.

## Solution
One new step: after installing optics in a cab, log the cab ID and count. Takes 5 seconds. Now every optic has a chain: delivery → box → checkout → cab. Discrepancies surface instantly with the last known custodian and exact cab.

## Before / After
| Before | After |
|--------|-------|
| "We're missing 2 optics somewhere" | "8 unaccounted from checkout #3 — Carlos, cabs B1-001 to B1-004" |
| Blame game between shifts | Audit trail with timestamps and names |
| Discovered at data hall (too late) | Caught at pre-staging (actionable) |

## Quick Start
```bash
open index.html
```
Demo data is pre-loaded with three scenarios: happy path, missing optics, and box discrepancy.

## CoreWeave Hackathon 2026
- **Track:** Build with Velocity
- **Team:** Romeo Patino — DCT, EVI01
