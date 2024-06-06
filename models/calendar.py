import datetime
import os.path
import logging

from rich.console import Console
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from helper.helper import display_event_details

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]
NOT_FOUND = "NOT_FOUND"

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
console = Console()


class Calendar:
    def __init__(self):
        self.creds = None
        self.service = None
        self.authenticate()

    def authenticate(self):
        """Handles user authentication and saves credentials."""
        if os.path.exists("token.json"):
            self.creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES
                )
                self.creds = flow.run_local_server(port=0)
            with open("token.json", "w") as token:
                token.write(self.creds.to_json())

        self.service = build("calendar", "v3", credentials=self.creds)

    def create_event(self, new_event):
        """Creates a new Event"""
        try:
            event = self.service.events().insert(calendarId='primary', body=new_event).execute()
            logger.info(f"Event created: {event.get('htmlLink')}")
            display_event_details([event])
        except HttpError as error:
            logger.error(f"An error occurred: {error}")

    def delete_event(self, e_id):
        """Deletes an Event provided by an event_Id (or e_id can be seen in the function argument)"""
        try:
            self.service.events().delete(calendarId='primary', eventId=e_id).execute()
            logger.info(f"Event with ID {e_id} deleted.")
        except HttpError as error:
            logger.error(f"An error occurred: {error}")
            return NOT_FOUND

    def get_event_by_id(self, e_id):
        """Get an Event provided by an event_id (or e_id can be seen in the function argument)"""
        try:
            event = self.service.events().get(calendarId='primary', eventId=e_id).execute()
            logger.info(f"The Event is: {event}")
            display_event_details([event])
            return event

        except HttpError as error:
            logger.error(f"An error occurred: {error}")
            return NOT_FOUND

    def get_events_by_summary(self, summary, result):
        f"""Get an Event by {summary}  (can be seen in the function argument)
    Here, using substring of {summary} fetches upcoming 5 events by default if {result}
    is not given. 
    """
        try:
            all_events = self.list_events(10000)
            events_matched_with_summary_substring = []
            for event in all_events:
                if summary.lower() in event.get('summary', '').lower():
                    events_matched_with_summary_substring.append(event)
                    if len(events_matched_with_summary_substring) >= result:
                        break
            display_event_details(events_matched_with_summary_substring)
        except HttpError as error:
            logger.error(f"An error occurred: {error}")
            return NOT_FOUND

    def update_event(self, updated_event):
        f"""Update an Event provided by an {updated_event} can be seen in the function argument"""
        try:
            event = self.get_event_by_id(updated_event['id'])
            logger.info(f"Before Update the Event is: {event}")
            new_processed_event = self.service.events().update(calendarId='primary', eventId=updated_event['id'],
                                                               body=updated_event).execute()
            logger.info(f"After Update the Event is: {new_processed_event}")
            display_event_details([event])
        except HttpError as error:
            logger.error(f"An error occurred: {error}")
            return NOT_FOUND

    def list_events(self, result):
        f"""Lists the upcoming events on the user's calendar.
            
        Finds {result} number of events from Calendar. If {result} variable is
        not provided(aka None), then it will show upcoming 10 events by default.
        """
        try:
            now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
            logger.info(f"Getting the upcoming {result} events")
            events_result = (
                self.service.events()
                .list(
                    calendarId="primary",
                    timeMin=now,
                    maxResults=result,
                    singleEvents=True,
                    orderBy="startTime",
                )
                .execute()
            )
            events = events_result.get("items", [])
            if not events:
                logger.info("No upcoming events found.")
                return

            display_event_details(events)
            logger.info(f"Found upcoming {len(events)} events")
            return events
        except HttpError as error:
            logger.error(f"An error occurred: {error}")

    def list_acls(self):
        """Lists the ACLs for the primary calendar."""
        try:
            acl = self.service.acl().list(calendarId='primary').execute()
            logger.info("Current ACLs:")
            for rule in acl['items']:
                logger.info(f"Scope: {rule['scope']}, Role: {rule['role']}, rule_id: {rule['id']}")

        except HttpError as error:
            logger.error(f"An error occurred while fetching the ACL list: {error}")

    def insert_acl(self, user_email: str, role: str):
        """Inserts an ACL rule for the primary calendar."""
        try:
            new_rule = {
                'scope': {
                    'type': 'user',
                    'value': user_email
                },
                'role': role
            }
            created_rule = self.service.acl().insert(calendarId='primary', body=new_rule).execute()
            logger.info(f"Inserted ACL rule: {created_rule}")

        except HttpError as error:
            logger.error(f"An error occurred while inserting the ACL rule: {error}")

    def delete_acl(self, rule_id: str):
        """Deletes an ACL rule for the primary calendar."""
        try:
            self.service.acl().delete(calendarId='primary', ruleId=rule_id).execute()
            logger.info(f"Deleted ACL rule with ID: {rule_id}")

        except HttpError as error:
            logger.error(f"An error occurred while deleting the ACL rule: {error}")
