# Decom Checklist

## One-Line
Guided decommission workflow — step-by-step with timestamps, nothing skipped, completion record generated at the end.

## Problem
Hardware decommissions have a specific ordered sequence (ticket verify → power down → cable removal → asset scan → staging log) but today it's tribal knowledge and paper. Mistakes — wrong serial logged, live cable pulled, ticket not updated — are common and expensive.

Who feels it: DCTs doing decommission work at EVI01
When: Every hardware pull, end-of-life removal, or rack rebuild
How often: Regularly during active decom campaigns — multiple nodes per shift

## What It Does
1. Enter ticket number + node/asset tag to start a decom session
2. App walks through each step in order — can't skip ahead
3. Each step: description, what to check, confirm button → timestamped
4. Flags steps with warnings (e.g. "verify power is off before cable removal")
5. End: generates a completion record (copy/paste or download) with all timestamps and asset info

## Demo Story
1. Normal decom — complete all steps → clean record generated, paste into ticket
2. Skip attempt — try to jump to cable removal before power-down step → blocked with warning
3. Mid-decom interruption — close app, reopen → session restored from localStorage, pick up where you left off

## Tech Stack
- Language: HTML/JS (single file, no backend)
- Data source: Static step definitions (JSON or hardcoded)
- UI: Mobile-first — DCTs are on the floor with phones, not laptops
- Persistence: localStorage for session resume

## File Structure
```
decom-checklist/
  index.html      # Full app — session start, step flow, record output
  steps.json      # Step definitions with warnings, confirmations, notes
```

## Status
- [ ] Step definitions written (steps.json)
- [ ] Core flow built (step progression, timestamps, block logic)
- [ ] Session resume from localStorage
- [ ] Record generation (copy-paste output)
- [ ] Demo scenarios scripted
- [ ] Slides done
- [ ] Video recorded

## Judging Track
Build with Velocity — reduces human error in physical ops, generates audit trail

## Winning Criteria Check
- [ ] Closes a loop — decom starts → every step logged → record in ticket
- [ ] Physical/DC-native — cable pulls, power down sequences, asset scans
- [ ] Shippable in 48h (single HTML file)
- [ ] Clear before/after story — tribal knowledge + paper → timestamped audit trail
- [ ] No finance data or politics needed

## Key Pitching Lines
- "Every decom that goes wrong starts with a step someone skipped"
- "This runs on your phone, in the aisle, offline"
- "The output is a paste-ready record — closes the Jira ticket in one copy"
