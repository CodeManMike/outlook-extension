---
description: Review unread inbox emails, classify them, and prepare drafts or category changes for review
argument-hint: "[limit, default 20]"
---

Triage the user's unread inbox:

1. Call `list_emails(unread_only=true, limit=$ARGUMENTS)` (default limit 20 if no argument).
2. For each email, call `read_email` to get the full body.
3. Classify each as one of:
   - **urgent** — needs a reply today
   - **reply** — needs a reply, not urgent
   - **fyi** — no action, just informational
   - **newsletter** — automated / promotional
   - **spam** — obvious junk
4. Present a table: sender · subject · classification · 1-line summary.
5. For each **urgent** and **reply**: draft a response via `create_draft(reply_mode="reply", body=...)`. Surface the draft text inline.
6. For each **newsletter**/**fyi**: propose a category via `list_categories` + `set_email_categories` or a folder move.

Do **not** send anything. Do **not** delete anything. Surface proposals for the user to approve.
