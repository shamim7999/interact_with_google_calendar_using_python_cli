import datetime
import logging
import typer
import helper.helper as helper


from typing_extensions import Annotated
from typing import List, Optional
from google_calendar.calendar import GoogleCalendar


app = typer.Typer()
calendar = GoogleCalendar()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.command()
def list_events(results: Optional[int] = 10):
    calendar.event.list_events(results)


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

    calendar.event.create_event(new_event)


@app.command()
def delete_event(event_id: str):
    calendar.event.delete_event(event_id)


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
    old_event = calendar.event.get_event_by_id(event_id)
    attendees = helper.get_attendees_field(old_event, attendees)
    summary = helper.get_summary_field(old_event, summary)
    description = helper.get_description_field(old_event, description)
    start = helper.get_start_field(old_event, start)
    end = helper.get_end_field(old_event, end)
    eligible_attendees = attendees + calendar.event.get_attendees(event_id)

    if ra:
        eligible_attendees = calendar.event.remove_attendees(attendees, eligible_attendees)

    logger.info(f"-----------------------\nAttendees----------------------: {eligible_attendees}\n---------------\n")
    updated_event = {
        'id': event_id,
        'summary': summary,
        'description': description,
        'start': {'dateTime': start, 'timeZone': 'UTC'},
        'end': {'dateTime': end, 'timeZone': 'UTC'},
        'attendees': eligible_attendees
    }

    calendar.event.update_event(updated_event)


@app.command()
def get_event_by_id(e_id: str):
    calendar.event.get_event_by_id(e_id)


@app.command()
def get_events_by_summary(summary: str, result: Optional[int] = 5):
    calendar.event.get_events_by_summary(summary, result)
    pass


@app.command()
def delete_event_by_summary(summary: str):
    calendar.event.delete_event_by_summary(summary)


@app.command()
def import_event(event_id: str, start: Optional[datetime.datetime], end: Optional[datetime.datetime] = None):
    calendar.event.import_event(event_id, start, end)


@app.command()
def get_event_instances(event_id: str):
    calendar.event.get_event_instances(event_id)


@app.command()
def update_event_instances(
        event_id: str,
        summary: Optional[str] = None,
        description: Optional[str] = None,
        attendees: Annotated[Optional[List[str]], typer.Option()] = None,
        ra: Optional[bool] = typer.Option(False, "--ra", help="Remove attendees")
):
    old_recurring_event = calendar.event.get_event_by_id(event_id)

    attendees = helper.get_attendees_field(old_recurring_event, attendees)
    summary = helper.get_summary_field(old_recurring_event, summary)
    description = helper.get_description_field(old_recurring_event, description)

    eligible_attendees = attendees + calendar.event.get_attendees(event_id)

    if ra:
        eligible_attendees = calendar.event.remove_attendees(attendees, eligible_attendees)

    logger.info(f"-----------------------\nAttendees----------------------: {eligible_attendees}\n---------------\n")
    updated_recurring_event = {
        'id': event_id,
        'summary': summary,
        'description': description,
        'attendees': eligible_attendees
    }
    logger.info(f"UPDATED_RECUR_EVENT: {updated_recurring_event}")
    calendar.event.update_event_instances(updated_recurring_event)


@app.command()
def watch_event(event_id: str):
    calendar.event.watch_event(event_id)


@app.command()
def list_acls():
    calendar.acl.list_acls()


@app.command()
def insert_acl(user_email: str, role: str):
    calendar.acl.insert_acl(user_email, role)


@app.command()
def delete_acl(rule_id: str):
    calendar.acl.delete_acl(rule_id)


if __name__ == "__main__":
    app()
