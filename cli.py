import datetime

import typer

from typing_extensions import Annotated
from typing import List, Optional
from models.calendar import Calendar

app = typer.Typer()


@app.command()
def list_events():
    calendar = Calendar()
    calendar.list_events()


@app.command()
def create_event(summary: str, description: str, start: datetime.datetime, end: datetime.datetime,
                 attendees: Annotated[Optional[List[str]], typer.Option()] = None):
    if attendees:
        attendees = [{'email': email} for email in attendees]
    new_event = {
        'summary': summary,
        'description': description,
        'start': {'dateTime': start.isoformat(), 'timeZone': 'UTC'},
        'end': {'dateTime': end.isoformat(), 'timeZone': 'UTC'},
        'attendees': attendees
    }
    calendar = Calendar()
    calendar.create_event(new_event)
    pass


@app.command()
def list_acls():
    calendar = Calendar()
    calendar.list_acls()


@app.command()
def insert_acl(user_email: str, role: str):
    calendar = Calendar()
    calendar.insert_acl(user_email, role)


@app.command()
def delete_acl(rule_id: str):
    calendar = Calendar()
    calendar.delete_acl(rule_id)


if __name__ == "__main__":
    app()
