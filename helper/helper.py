import logging

from rich.console import Console
from rich.table import Table


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
console = Console()


def display_event_details(events):
    """Formats and displays event details in a table."""
    table = Table("ID", "Summary", "Description", "Start Time", "End Time", "Attendees Emails")
    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        end = event["end"].get("dateTime", event["end"].get("date"))
        summary = event.get("summary", "No Title Available")
        attendees = event.get("attendees", [])

        attendees_emails = [attendee.get("email", "No Email Available") for attendee in attendees]
        attendees_emails_str = ", ".join(attendees_emails)
        description = event.get("description", "No Description Available.")
        event_id = event['id']

        table.add_row(
            event_id,
            summary,
            description,
            start,
            end,
            attendees_emails_str
        )
        logger.info(f"Starting Time: {start}, Ending Time: {end}, Summary: {summary}, "
                    f"Attendees Email: {attendees_emails}")
    console.print(table)
