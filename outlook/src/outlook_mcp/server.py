"""MCP server exposing Outlook COM operations to Claude."""
from __future__ import annotations

from typing import Literal

from mcp.server.fastmcp import FastMCP

from . import outlook as ol

mcp = FastMCP("outlook")


# ---------- Accounts / folders ----------

@mcp.tool()
def list_accounts() -> list[dict]:
    """List Outlook accounts configured in the current profile."""
    return ol.list_accounts()


@mcp.tool()
def list_folders(account: str | None = None, recursive: bool = True) -> list[dict]:
    """List mail folders. Pass an account name to limit to one store."""
    return ol.list_folders(account=account, recursive=recursive)


# ---------- Email ----------

@mcp.tool()
def list_emails(
    folder: str | None = None,
    limit: int = 50,
    unread_only: bool = False,
    from_filter: str | None = None,
    subject_filter: str | None = None,
    since: str | None = None,
    before: str | None = None,
    newest_first: bool = True,
) -> list[dict]:
    """List emails in a folder.

    Args:
        folder: Path like "inbox", "inbox/Processed", or "account@x.com/Inbox".
            Defaults to the default Inbox.
        limit: Max emails to return.
        unread_only: If true, only unread emails.
        from_filter: Substring match against sender name or email.
        subject_filter: Substring match against subject.
        since: ISO 8601 datetime — only emails received at/after this time.
        before: ISO 8601 datetime — only emails received before this time.
        newest_first: Sort order.
    """
    return ol.list_emails(
        folder=folder, limit=limit, unread_only=unread_only,
        from_filter=from_filter, subject_filter=subject_filter,
        since=since, before=before, newest_first=newest_first,
    )


@mcp.tool()
def read_email(entry_id: str, store_id: str | None = None) -> dict:
    """Get full body, recipients, and attachment metadata for an email."""
    return ol.read_email(entry_id=entry_id, store_id=store_id)


@mcp.tool()
def search_emails(
    query: str,
    folder: str | None = None,
    limit: int = 50,
) -> list[dict]:
    """Substring search across subject, sender, and body within a folder."""
    return ol.search_emails(query=query, folder=folder, limit=limit)


@mcp.tool()
def move_email(
    entry_id: str,
    target_folder: str,
    store_id: str | None = None,
) -> dict:
    """Move an email to another folder. target_folder uses the same path format as list_emails."""
    return ol.move_email(entry_id=entry_id, target_folder=target_folder, store_id=store_id)


@mcp.tool()
def delete_email(
    entry_id: str,
    store_id: str | None = None,
    permanent: bool = False,
) -> dict:
    """Delete an email. By default moves to Deleted Items; set permanent=True to hard delete."""
    return ol.delete_email(entry_id=entry_id, store_id=store_id, permanent=permanent)


# ---------- Drafts / Send ----------

@mcp.tool()
def create_draft(
    to: list[str] | None = None,
    cc: list[str] | None = None,
    bcc: list[str] | None = None,
    subject: str | None = None,
    body: str | None = None,
    html_body: str | None = None,
    attachments: list[str] | None = None,
    reply_to_entry_id: str | None = None,
    reply_to_store_id: str | None = None,
    reply_mode: Literal["reply", "reply_all", "forward"] | None = None,
    importance: Literal["low", "normal", "high"] = "normal",
    categories: list[str] | None = None,
) -> dict:
    """Create a draft email, saved to Drafts. Does not send.

    For a reply or forward, pass reply_to_entry_id plus reply_mode. The draft
    inherits the quoted body; pass body/html_body to prepend your text.
    """
    return ol.create_draft(
        to=to, cc=cc, bcc=bcc, subject=subject, body=body, html_body=html_body,
        attachments=attachments, reply_to_entry_id=reply_to_entry_id,
        reply_to_store_id=reply_to_store_id, reply_mode=reply_mode,
        importance=importance, categories=categories,
    )


@mcp.tool()
def update_draft(
    entry_id: str,
    store_id: str | None = None,
    to: list[str] | None = None,
    cc: list[str] | None = None,
    bcc: list[str] | None = None,
    subject: str | None = None,
    body: str | None = None,
    html_body: str | None = None,
    add_attachments: list[str] | None = None,
    importance: Literal["low", "normal", "high"] | None = None,
    categories: list[str] | None = None,
) -> dict:
    """Edit an existing draft. Only provided fields are changed."""
    return ol.update_draft(
        entry_id=entry_id, store_id=store_id, to=to, cc=cc, bcc=bcc,
        subject=subject, body=body, html_body=html_body,
        add_attachments=add_attachments, importance=importance,
        categories=categories,
    )


@mcp.tool()
def send_email(
    entry_id: str | None = None,
    store_id: str | None = None,
    to: list[str] | None = None,
    cc: list[str] | None = None,
    bcc: list[str] | None = None,
    subject: str | None = None,
    body: str | None = None,
    html_body: str | None = None,
    attachments: list[str] | None = None,
    importance: Literal["low", "normal", "high"] = "normal",
) -> dict:
    """Send an email. Pass entry_id to send an existing draft, or pass to+subject
    (and optionally body/html_body/attachments) to compose and send in one call."""
    return ol.send_email(
        entry_id=entry_id, store_id=store_id, to=to, cc=cc, bcc=bcc,
        subject=subject, body=body, html_body=html_body,
        attachments=attachments, importance=importance,
    )


# ---------- Categories ----------

@mcp.tool()
def list_categories() -> list[dict]:
    """List the workspace master category list (name, color, shortcut)."""
    return ol.list_categories()


@mcp.tool()
def set_email_categories(
    entry_id: str,
    categories: list[str],
    mode: Literal["replace", "add", "remove"] = "replace",
    store_id: str | None = None,
) -> dict:
    """Set categories on an email. mode=add/remove to merge with existing."""
    return ol.set_email_categories(
        entry_id=entry_id, categories=categories, mode=mode, store_id=store_id,
    )


@mcp.tool()
def set_event_categories(
    entry_id: str,
    categories: list[str],
    mode: Literal["replace", "add", "remove"] = "replace",
    store_id: str | None = None,
) -> dict:
    """Set categories on a calendar event. mode=add/remove to merge with existing."""
    return ol.set_event_categories(
        entry_id=entry_id, categories=categories, mode=mode, store_id=store_id,
    )


# ---------- Calendar ----------

@mcp.tool()
def list_calendar_events(
    start: str,
    end: str,
    calendar: str | None = None,
    limit: int = 100,
) -> list[dict]:
    """List calendar events in a time range (ISO 8601). Expands recurring events."""
    return ol.list_calendar_events(start=start, end=end, calendar=calendar, limit=limit)


@mcp.tool()
def create_calendar_event(
    subject: str,
    start: str,
    end: str,
    body: str | None = None,
    location: str | None = None,
    attendees: list[str] | None = None,
    categories: list[str] | None = None,
    all_day: bool = False,
    is_meeting: bool = False,
    reminder_minutes: int | None = None,
) -> dict:
    """Create a calendar event. If attendees is set (or is_meeting=True),
    the event is sent as a meeting invite."""
    return ol.create_calendar_event(
        subject=subject, start=start, end=end, body=body, location=location,
        attendees=attendees, categories=categories, all_day=all_day,
        is_meeting=is_meeting, reminder_minutes=reminder_minutes,
    )


@mcp.tool()
def update_calendar_event(
    entry_id: str,
    store_id: str | None = None,
    subject: str | None = None,
    start: str | None = None,
    end: str | None = None,
    body: str | None = None,
    location: str | None = None,
    add_attendees: list[str] | None = None,
    categories: list[str] | None = None,
    send_update: bool = False,
) -> dict:
    """Update a calendar event. Set send_update=True to notify attendees."""
    return ol.update_calendar_event(
        entry_id=entry_id, store_id=store_id, subject=subject, start=start, end=end,
        body=body, location=location, add_attendees=add_attendees,
        categories=categories, send_update=send_update,
    )


@mcp.tool()
def delete_calendar_event(entry_id: str, store_id: str | None = None) -> dict:
    """Delete a calendar event."""
    return ol.delete_calendar_event(entry_id=entry_id, store_id=store_id)


@mcp.tool()
def respond_to_invite(
    entry_id: str,
    response: Literal["accept", "tentative", "decline"],
    send_response: bool = True,
    store_id: str | None = None,
) -> dict:
    """Respond to a meeting invite. send_response=False saves the response without notifying the organizer."""
    return ol.respond_to_invite(
        entry_id=entry_id, response=response,
        send_response=send_response, store_id=store_id,
    )


# ---------- Contacts ----------

@mcp.tool()
def list_contacts(
    search: str | None = None,
    folder: str | None = None,
    limit: int = 100,
) -> list[dict]:
    """List contacts. Pass search to filter by name, email, or company."""
    return ol.list_contacts(search=search, folder=folder, limit=limit)


@mcp.tool()
def get_contact(entry_id: str, store_id: str | None = None) -> dict:
    """Get full details for a contact."""
    return ol.get_contact(entry_id=entry_id, store_id=store_id)


@mcp.tool()
def create_contact(
    full_name: str | None = None,
    first_name: str | None = None,
    last_name: str | None = None,
    email1: str | None = None,
    email2: str | None = None,
    email3: str | None = None,
    company: str | None = None,
    job_title: str | None = None,
    department: str | None = None,
    business_phone: str | None = None,
    home_phone: str | None = None,
    mobile_phone: str | None = None,
    business_address: str | None = None,
    home_address: str | None = None,
    notes: str | None = None,
    categories: list[str] | None = None,
) -> dict:
    """Create a new contact in the default Contacts folder."""
    return ol.create_contact(
        full_name=full_name, first_name=first_name, last_name=last_name,
        email1=email1, email2=email2, email3=email3, company=company,
        job_title=job_title, department=department, business_phone=business_phone,
        home_phone=home_phone, mobile_phone=mobile_phone,
        business_address=business_address, home_address=home_address,
        notes=notes, categories=categories,
    )


@mcp.tool()
def update_contact(
    entry_id: str,
    store_id: str | None = None,
    full_name: str | None = None,
    first_name: str | None = None,
    last_name: str | None = None,
    email1: str | None = None,
    email2: str | None = None,
    email3: str | None = None,
    company: str | None = None,
    job_title: str | None = None,
    department: str | None = None,
    business_phone: str | None = None,
    home_phone: str | None = None,
    mobile_phone: str | None = None,
    business_address: str | None = None,
    home_address: str | None = None,
    notes: str | None = None,
    categories: list[str] | None = None,
) -> dict:
    """Update an existing contact. Only provided fields are changed."""
    return ol.update_contact(
        entry_id=entry_id, store_id=store_id,
        full_name=full_name, first_name=first_name, last_name=last_name,
        email1=email1, email2=email2, email3=email3, company=company,
        job_title=job_title, department=department, business_phone=business_phone,
        home_phone=home_phone, mobile_phone=mobile_phone,
        business_address=business_address, home_address=home_address,
        notes=notes, categories=categories,
    )


@mcp.tool()
def delete_contact(
    entry_id: str,
    store_id: str | None = None,
    permanent: bool = False,
) -> dict:
    """Delete a contact. By default moves to Deleted Items; set permanent=True to hard delete."""
    return ol.delete_contact(entry_id=entry_id, store_id=store_id, permanent=permanent)


# ---------- Tasks ----------

@mcp.tool()
def list_tasks(
    folder: str | None = None,
    include_completed: bool = False,
    due_before: str | None = None,
    due_after: str | None = None,
    limit: int = 100,
) -> list[dict]:
    """List tasks. Filters: include_completed, due_before/due_after (ISO 8601)."""
    return ol.list_tasks(
        folder=folder, include_completed=include_completed,
        due_before=due_before, due_after=due_after, limit=limit,
    )


@mcp.tool()
def get_task(entry_id: str, store_id: str | None = None) -> dict:
    """Get full details for a task including body."""
    return ol.get_task(entry_id=entry_id, store_id=store_id)


@mcp.tool()
def create_task(
    subject: str,
    body: str | None = None,
    due_date: str | None = None,
    start_date: str | None = None,
    status: Literal["not_started", "in_progress", "complete", "waiting", "deferred"] = "not_started",
    priority: Literal["low", "normal", "high"] = "normal",
    reminder_date: str | None = None,
    categories: list[str] | None = None,
) -> dict:
    """Create a new task."""
    return ol.create_task(
        subject=subject, body=body, due_date=due_date, start_date=start_date,
        status=status, priority=priority, reminder_date=reminder_date,
        categories=categories,
    )


@mcp.tool()
def update_task(
    entry_id: str,
    store_id: str | None = None,
    subject: str | None = None,
    body: str | None = None,
    due_date: str | None = None,
    start_date: str | None = None,
    status: Literal["not_started", "in_progress", "complete", "waiting", "deferred"] | None = None,
    priority: Literal["low", "normal", "high"] | None = None,
    reminder_date: str | None = None,
    categories: list[str] | None = None,
) -> dict:
    """Update an existing task. Only provided fields are changed."""
    return ol.update_task(
        entry_id=entry_id, store_id=store_id, subject=subject, body=body,
        due_date=due_date, start_date=start_date, status=status, priority=priority,
        reminder_date=reminder_date, categories=categories,
    )


@mcp.tool()
def complete_task(entry_id: str, store_id: str | None = None) -> dict:
    """Mark a task as complete (100%)."""
    return ol.complete_task(entry_id=entry_id, store_id=store_id)


@mcp.tool()
def delete_task(
    entry_id: str,
    store_id: str | None = None,
    permanent: bool = False,
) -> dict:
    """Delete a task. By default moves to Deleted Items; set permanent=True to hard delete."""
    return ol.delete_task(entry_id=entry_id, store_id=store_id, permanent=permanent)


# ---------- Attachments ----------

@mcp.tool()
def save_attachment(
    entry_id: str,
    attachment_index: int,
    save_path: str,
    store_id: str | None = None,
) -> dict:
    """Save an email attachment to disk.

    Args:
        entry_id: EntryID of the email (from list_emails or read_email).
        attachment_index: 1-based index matching the attachments list in read_email.
        save_path: Destination file path or directory. If a directory is given,
            the attachment's original filename is used. Supports ~ and %USERPROFILE%.
        store_id: Optional store ID to pair with entry_id.
    """
    return ol.save_attachment(
        entry_id=entry_id, attachment_index=attachment_index,
        save_path=save_path, store_id=store_id,
    )


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
