---
description: Find an email and draft a reply for user review
argument-hint: "<search query to locate the email>"
---

Find and draft a reply:

1. Call `search_emails(query="$ARGUMENTS", limit=5)`.
2. If multiple results, show them and ask which one.
3. Call `read_email` on the chosen message to get full context.
4. Call `create_draft(reply_to_entry_id=..., reply_to_store_id=..., reply_mode="reply", body=...)` with a thoughtful reply that matches the user's tone from prior correspondence if visible.
5. Show the drafted reply inline and ask whether to send, edit, or discard.

Do not call `send_email` until the user explicitly confirms.
