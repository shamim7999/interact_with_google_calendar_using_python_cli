import os.path
import logging
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from features.event import Event
from features.acl import ACL

SCOPES = ["https://www.googleapis.com/auth/calendar"]
NOT_FOUND = "NOT_FOUND"

logger = logging.getLogger(__name__)


class GoogleCalendar:
    def __init__(self):
        self.creds = None
        self.service = None
        self.authenticate()
        self.event = Event(self.service)
        self.acl = ACL(self.service)

    def authenticate(self):
        """Handles user authentication and saves credentials."""
        try:
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
        except HttpError as error:
            logger.error(f"Error found while authenticating.")
