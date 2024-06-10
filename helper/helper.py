import logging
import json

from rich.console import Console
from rich.table import Table

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
console = Console()


def display_event_details(events):
    """Formats and displays event details in a table."""
    table = Table("ID", "Summary", "Description", "Start Time", "End Time", "Attendees Emails", "Event Type")
    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        end = event["end"].get("dateTime", event["end"].get("date"))
        summary = event.get("summary", "No Title Available")
        attendees = event.get("attendees", [])

        attendees_emails = [attendee.get("email", "No Email Available") for attendee in attendees]
        attendees_emails_str = ", ".join(attendees_emails)
        description = event.get("description", "No Description Available.")
        event_id = event['id']
        event_type = event.get('eventType', 'N/A')

        table.add_row(
            event_id,
            summary,
            description,
            start,
            end,
            attendees_emails_str,
            event_type
        )
        logger.info(f"Starting Time: {start}, Ending Time: {end}, Summary: {summary}, "
                    f"Attendees Email: {attendees_emails}")
        logger.info(f"{json.dumps(event, indent=2)}\n")
    console.print(table)


def get_summary_field(old_event, summary):
    if summary is None:
        summary = old_event.get('summary', "Summary Not Available.")
    return summary


def get_attendees_field(old_event, attendees):
    if attendees:
        attendees = [{'email': email} for email in attendees]
    else:
        attendees = old_event.get('attendees', "Attendees Not Available.")
    return attendees


def get_description_field(old_event, description):
    if description is None:
        description = old_event.get('description', "description Not Available.")
    return description


def get_start_field(old_event, start):
    if start is None:
        start = old_event['start'].get('dateTime', "Start Not Available.")
    else:
        start = start.isoformat()
    return start


def get_end_field(old_event, end):
    if end is None:
        end = old_event['end'].get('dateTime', "Start Not Available.")
    else:
        end = end.isoformat()
    return end