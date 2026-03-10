# Carrier Email Parser

> Auto-classify carrier maintenance emails, identify CW vs carrier responsibility, and draft responses for backbone events.

## Problem

Network Ops teams process dozens of carrier emails per shift — maintenance windows, outage alerts, circuit issues. Each one requires:
- Reading and classifying the email type
- Checking if it affects CoreWeave infrastructure
- Deciding who needs to act (CW or carrier)
- Drafting a response

This is slow, repetitive, and things get missed under volume.

## Solution

A parser that:
1. Ingests carrier emails (static samples for demo, `gws gmail` for live)
2. Classifies each as Maintenance / Outage / Circuit Issue / Info Only
3. Maps affected circuits to CW sites
4. Triages as CW-action / carrier-action / info-only
5. Drafts a templated response

## Demo

Three scenarios showing the full loop:
1. Planned maintenance → acknowledge
2. Unplanned outage → escalate
3. Carrier requesting info → respond with stats

## Stack

Python + HTML dashboard. Static data for demo. Claude/Gemini API for classification.

## Status

Concept phase. Depends on `gws` CLI approval for live email access.

---

CoreWeave Hackathon 2026 — Productivity at Scale
