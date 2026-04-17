---
description: Identify stale or low-value emails for batch archival or deletion
argument-hint: "[days old, default 14]"
---

Help the user clean up the inbox:

1. Compute the cutoff date as (today - $ARGUMENTS days), default 14 if no argument.
2. Call `list_emails(folder="inbox", before=cutoff_iso, limit=100, newest_first=false)`.
3. Group the results:
   - **Newsletters / automated** — sender looks like `noreply@`, `newsletter@`, `marketing@`, `updates@`, etc.
   - **Read but untouched** — unread=false, no category, no follow-up
   - **Unread and old** — probably never going to be read
4. For each group, propose an action (delete, move to Archive, categorize), show counts, and ask the user to confirm per-group — NOT per-email.
5. On confirmation, execute via `delete_email` (permanent=false) or `move_email`.

Never delete without explicit user confirmation for the group.
