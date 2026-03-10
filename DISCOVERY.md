# DCT Pain Point Discovery
_Goal: Find real problems to build around. Answer "what do DCTs wish they had a tool for?"_

---

## Where to Search (Priority Order)

### 1. Slack (highest signal)
Search these channels and keywords:

**Channels to check:**
- `#ops-us-central-07a-us-evi01-elk-grove` — your hall's ops channel
- `#dct` or `#dc-technicians` or `#field-ops` — DCT-specific
- `#net-backbone` — backbone issues
- `#more-faster-better-2026` — hackathon channel (others may have already posted ideas)
- `#evi01` or `#elk-grove` — site-specific
- Any `#incident-*` or `#oncall-*` channels

**Keywords to search (Slack search bar: `in:#channel keyword`):**
```
"wish we had"
"should be automated"
"anyone know where"
"who owns"
"takes forever"
"every time"
"annoying"
"manual process"
"tribal knowledge"
"DCT"
"walking"
"spare"
"optic"
"cable"
"uplink"
"FBS"
"BMC"
"ticket"
"stale"
"confusing"
```

### 2. Jira
Search for:
- Your own past tickets — what types recur? what took longest?
- Tickets with "DCT" in the description
- Tickets that bounced between teams multiple times
- Tickets that took >8 hours to resolve
- Labels: `dct`, `dc-ops`, `manual`, `floor-ops`

**Jira filters to try:**
```
project = DC AND assignee = currentUser ORDER BY created DESC
project = DC AND comment ~ "tribal knowledge"
project = DC AND timespent > 8h AND type = "Service Request"
project = DC AND labels = DCT
```

### 3. Confluence / Internal Docs
- Search "DCT runbook" — what runbooks exist? what don't?
- Search "EVI01 known issues"
- Search "cable" + "maintenance" + "risk"
- Look for any "lessons learned" docs from past incidents

### 4. Ask 3 People Directly
The fastest research is just asking 2-3 colleagues:
> "What's the one thing you do manually that you wish was automated or faster?"

Target:
- [ ] Another DCT on your team
- [ ] A NetEng who works with you
- [ ] NOC person who handles your site's tickets

---

## Questions to Answer (Your Gap List)

### About Your Own Pain
- [ ] What type of ticket do you personally dread getting?
- [ ] What do you have to look up every time instead of knowing by heart?
- [ ] What's the last thing you thought "this is a waste of my time"?
- [ ] When was the last time something took way longer than it should have?
- [ ] What do new DCTs always ask you about?
- [ ] What's confusing about your hall to people who haven't worked it?

### About Workflows
- [ ] What's the handoff between shifts like? What gets lost?
- [ ] How do you figure out what a ticket needs before you go to the floor?
- [ ] How long does it take to find spare parts?
- [ ] How do you know if a cable pull is "safe" right now?
- [ ] How do you communicate blast radius to other teams today?
- [ ] What info do you always have to manually look up before touching something?

### About Tools You Already Use
- [ ] What tools do you use daily? (Jira, Slack, DCIM, Grafana, internal portals?)
- [ ] Which ones are slow, broken, or annoying?
- [ ] What do you do in a spreadsheet that should probably be a real tool?
- [ ] What do you copy-paste constantly?

### About Physical Reality
- [ ] Which rack/row generates the most tickets at EVI01?
- [ ] Which hardware fails most often?
- [ ] What's the most dangerous physical operation you do regularly?
- [ ] What do you always check before touching backbone gear?
- [ ] Where are spares stored and is that location optimal?

### About Knowledge Gaps
- [ ] What do new DCTs take the longest to learn?
- [ ] What documentation is outdated or missing?
- [ ] What's in your head that isn't written down anywhere?

---

## What to Do With Your Answers

Once you've gathered intel, categorize each pain into:

| Pain | How Often | Time Lost | Could a Tool Fix It? | Data Available? |
|------|-----------|-----------|---------------------|-----------------|
|      |           |           |                     |                 |

Then pick the one where:
- **How Often** = frequent (weekly or daily)
- **Time Lost** = meaningful (>5 min per occurrence)
- **Could a Tool Fix It** = yes, with static data or simple logic
- **Data Available** = you can get or fake it for a demo

That's your project.

---

## Recommended Next Actions

1. **Today:** Search Slack for the keywords above. Paste anything interesting here.
2. **Today:** Open Jira, look at your last 20 tickets. Note patterns.
3. **Before March 12:** Ask 2 colleagues the "one thing you wish was automated" question.
4. **By March 15:** Fill in the pain table above and pick your project.

---

## Notes (paste findings here as you go)

_Add Slack snippets, Jira ticket patterns, colleague quotes here_

```
[date] - source - finding
```
