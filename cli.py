import datetime
import logging
import typer
import json

from typing_extensions import Annotated
from typing import List, Optional
from google_calendar.calendar import GoogleCalendar

app = typer.Typer()
calendar = GoogleCalendar()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.command()
def list_events(results: Optional[int] = 10):
    calendar.list_events(results)


@app.command()
def create_event(summary: str, description: str, start: datetime.datetime, end: datetime.datetime,
                 attendees: Annotated[Optional[List[str]], typer.Option()] = None,
                 recur: Optional[str] = None):
    if attendees:
        attendees = [{'email': email} for email in attendees]
    new_event = {
        'summary': summary,
        'description': description,
        'start': {'dateTime': start.isoformat(), 'timeZone': 'UTC'},
        'end': {'dateTime': end.isoformat(), 'timeZone': 'UTC'},
        'attendees': attendees,
        'recurrence': []
    }

    if recur is not None:
        if recur.lower() == 'monthly':
            new_event['recurrence'] = ['RRULE:FREQ=MONTHLY;COUNT=12;BYMONTHDAY=1']
        if recur.lower() == 'daily':
            new_event['recurrence'] = ['RRULE:FREQ=DAILY;COUNT=2']

    calendar.create_event(new_event)


@app.command()
def delete_event(event_id: str):
    calendar.delete_event(event_id)


@app.command()
def update_event(
        event_id: str,
        summary: Optional[str] = None,
        description: Optional[str] = None,
        start: Optional[datetime.datetime] = None,
        end: Optional[datetime.datetime] = None,
        attendees: Annotated[Optional[List[str]], typer.Option()] = None,
        ra: Optional[bool] = typer.Option(False, "--ra", help="Remove attendees")
):
    old_event = calendar.get_event_by_id(event_id)

    if attendees:
        attendees = [{'email': email} for email in attendees]
    else:
        attendees = old_event.get('attendees', "Attendees Not Available.")

    if summary is None:
        summary = old_event.get('summary', "Summary Not Available.")
    if description is None:
        description = old_event.get('description', "Description Not Available.")
    if start is None:
        start = old_event['start'].get('dateTime', "Start Not Available.")
    else:
        start = start.isoformat()
    if end is None:
        end = old_event['end'].get('dateTime', "End Not Available.")
    else:
        end = end.isoformat()

    eligible_attendees = attendees + calendar.get_attendees(event_id)

    if ra:
        eligible_attendees = calendar.remove_attendees(attendees, eligible_attendees)

    logger.info(f"-----------------------\nAttendees----------------------: {eligible_attendees}\n---------------\n")
    updated_event = {
        'id': event_id,
        'summary': summary,
        'description': description,
        'start': {'dateTime': start, 'timeZone': 'UTC'},
        'end': {'dateTime': end, 'timeZone': 'UTC'},
        'attendees': eligible_attendees
    }

    calendar.update_event(updated_event)


@app.command()
def get_event_by_id(e_id: str):
    calendar.get_event_by_id(e_id)


@app.command()
def get_events_by_summary(summary: str, result: Optional[int] = 5):
    calendar.get_events_by_summary(summary, result)
    pass


@app.command()
def import_event(event_id: str, start: Optional[datetime.datetime], end: Optional[datetime.datetime] = None):
    calendar.import_event(event_id, start, end)


@app.command()
def get_event_instances(event_id: str):
    calendar.get_event_instances(event_id)


@app.command()
def update_event_instances(
        event_id: str,
        summary: Optional[str] = None,
        description: Optional[str] = None,
        start: Optional[datetime.datetime] = None,
        end: Optional[datetime.datetime] = None,
        attendees: Annotated[Optional[List[str]], typer.Option()] = None,
        ra: Optional[bool] = typer.Option(False, "--ra", help="Remove attendees")
):

    pass

@app.command()
def watch_event(event_id: str):
    calendar.watch_event(event_id)


@app.command()
def list_acls():
    calendar.list_acls()


@app.command()
def insert_acl(user_email: str, role: str):
    calendar.insert_acl(user_email, role)


@app.command()
def delete_acl(rule_id: str):
    calendar.delete_acl(rule_id)


if __name__ == "__main__":
    app()
