---
description: Produce a morning digest of today's calendar and overnight email
---

Generate a daily briefing for the user:

1. **Calendar** — call `list_calendar_events(start=today_00:00, end=tomorrow_00:00)` and list each event with start time, duration, subject, location, and attendee count.
2. **Overnight email** — call `list_emails(folder="inbox", since=yesterday_17:00, limit=50)` and group by:
   - Replies needed (direct messages requiring response)
   - Notable FYI (mentions, internal updates)
   - Newsletters / promotional (count only)
3. **Open threads** — call `list_emails(folder="sent", limit=20)` to spot messages the user sent >2 days ago without a reply arriving back.

Format as a crisp morning brief, not a dump. Lead with what the user needs to act on today. Use ISO datetimes computed against the system clock — do not hard-code dates.
