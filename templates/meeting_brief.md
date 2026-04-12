# Meeting Prep Brief Template

> Sent 60 minutes before external meetings via Telegram.

## Format

```
**Meeting Prep: {meeting title}**
{time} | {location/link}

**Attendees**
- {name} -- {role, relationship context}

**Last Interaction**
- {date}: {what was discussed, any commitments made}

**Open Items**
- {anything pending between you and these people}

**Context**
- {relevant recent news, emails, or updates about them/their org}

**Suggested Talking Points**
1. {based on open items and context}
2. {based on relationship stage}
3. {based on your current priorities}
```

## Rules
- Only generate for external meetings (skip internal standups, 1:1s with direct reports unless flagged).
- If no prior history exists, note that: "First meeting. No prior context."
- Pull from email threads if relevant correspondence exists.
- For recurring meetings, note what changed since last time.

## Data Sources
1. Google Calendar (via MCP) -- event details and attendees
2. `memory/people/{person}.md` -- relationship context
3. Gmail (via MCP) -- recent threads with attendees
4. `tasks/active.md` -- open items involving attendees
5. `memory/daily/` -- recent daily notes mentioning attendees
