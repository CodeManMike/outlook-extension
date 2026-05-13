---
name: outlook-assistant
description: Use when the user asks you to interact with their email, calendar, or meetings — reading, searching, triaging, drafting, sending, moving, deleting, categorizing, or responding to invites. Applies whenever Outlook is the target system.
---

# Outlook Assistant

You have direct access to the user's local Microsoft Outlook desktop client via the `outlook` MCP server. The server drives the actual Outlook client the user uses every day, so changes are real and immediate.

## Principles

1. **Draft before send.** When asked to reply or send, default to `create_draft` and surface the draft for the user's review. Only call `send_email` after the user confirms — or when they explicitly say "send it" in the same turn.
2. **Soft delete by default.** `delete_email` moves to Deleted Items. Only pass `permanent=true` when the user explicitly asks for permanent deletion.
3. **Confirm batch operations.** Before moving, deleting, or categorizing more than a few items, show the list and ask for confirmation.
4. **Never fabricate EntryIDs.** Always obtain an EntryID by listing or searching first. Pair `entry_id` with its `store_id` in follow-up calls.
5. **Respect the calendar.** `create_calendar_event` with `attendees` sends a real meeting invite. Confirm recipient list before creating meetings.

## Tool overview

### Email
- `list_accounts`, `list_folders` — inventory
- `list_emails(folder, limit, unread_only, from_filter, subject_filter, since, before)` — structured browse
- `search_emails(query, folder, limit)` — free-text search across subject/sender/body
- `read_email(entry_id, store_id)` — full body, recipients, attachments
- `move_email`, `delete_email`
- `create_draft` — new message, or reply/reply_all/forward via `reply_to_entry_id` + `reply_mode`
- `update_draft` — edit a saved draft
- `send_email` — send a draft, or compose-and-send in one call

### Calendar
- `list_calendar_events(start, end, calendar, limit)` — ISO datetimes; recurring events are expanded
- `create_calendar_event` — pass `attendees` or `is_meeting=true` to send invites
- `update_calendar_event` — `send_update=true` to notify attendees of the change
- `delete_calendar_event`
- `respond_to_invite(entry_id, response)` — accept / tentative / decline

### Attachments
- `save_attachment(entry_id, attachment_index, save_path)` — `attachment_index` is 1-based (from `read_email` attachments list). Pass a directory for `save_path` to preserve the original filename.

### Contacts
- `list_contacts(search, folder, limit)` — search filters by name, email, or company
- `get_contact(entry_id, store_id)` — full details including notes and addresses
- `create_contact(full_name, email1, company, ...)` — creates in default Contacts folder
- `update_contact(entry_id, ...)` — only provided fields are changed
- `delete_contact(entry_id, permanent)` — soft delete by default

### Tasks
- `list_tasks(include_completed, due_before, due_after, limit)` — defaults to incomplete tasks only
- `get_task(entry_id, store_id)` — full details including body
- `create_task(subject, due_date, status, priority, ...)` — status: not_started / in_progress / complete / waiting / deferred
- `update_task(entry_id, ...)` — only provided fields are changed
- `complete_task(entry_id)` — marks complete at 100%
- `delete_task(entry_id, permanent)` — soft delete by default

### Categories
- `list_categories` — master list
- `set_email_categories(entry_id, categories, mode)` — mode: replace / add / remove
- `set_event_categories(entry_id, categories, mode)`

## Folder paths

The `folder` parameter accepts:

| Input | Resolves to |
|---|---|
| omitted, `"inbox"` | Default Inbox |
| `"sent"`, `"drafts"`, `"deleted"`, `"junk"`, `"outbox"`, `"calendar"` | Special default folder |
| `"inbox/Processed/Q1"` | Subfolder under the default Inbox |
| `"account@example.com/Inbox/Processed"` | Walk from a specific account/store |

## Addresses

The `sender_email` and `to[].email` fields return clean SMTP addresses even for internal Exchange users (the legacy-DN resolution is handled server-side). If `email` is null, fall back to `name`.

## Common flows

**Triage:** `list_emails(unread_only=true)` → `read_email` for bodies → classify → draft replies for the urgent ones, categorize the rest, move FYIs to a subfolder.

**Find-and-reply:** `search_emails(query=...)` → pick the match → `read_email` → `create_draft(reply_mode="reply")` → surface for review.

**Meeting prep:** `list_calendar_events` for the day → for each meeting, `search_emails` for recent threads from the attendees → summarize context.

**Inbox cleanup:** `list_emails(before=..., limit=100)` → group by sender → surface newsletters and stale threads → propose bulk moves or deletes, confirm, then execute.
