import datetime
import logging

from googleapiclient.errors import HttpError
from helper.helper import display_event_details, display_calendar_details

logger = logging.getLogger(__name__)
NOT_FOUND = 'NOT_FOUND'


class CalendarList:
    def __init__(self, service):
        self.service = service

    def list_calendars(self):
        """
        Retrieves and lists all calendars associated with the authenticated Google account.

        This method uses the calendarList().list() feature of the Google Calendar API
        to fetch all calendars in the user's calendar list.

        Returns:
            list: A list of calendar summaries and their corresponding IDs.

        Raises:
            HttpError: If the request to the Google Calendar API fails.

        Logs:
            The details of the calendars using the logger.
        """
        try:
            calendar_list = self.service.calendarList().list().execute()
            calendars = calendar_list.get('items', [])

            if not calendars:
                print('No calendars found.')
                logger.info('No calendars found.')
                return []

            calendar_details = [{'id': calendar['id'], 'summary': calendar['summary']} for calendar in calendars]
            for calendar_detail in calendar_details:
                logger.info(f"CALENDARS: {calendar_detail}\n")
            display_calendar_details(calendar_details)
            return calendar_details

        except HttpError as error:
            logger.error(f"HTTP Error found {error}")
        except OSError as error:
            logger.error(f"OS Error found {error}")
        except Exception as error:
            logger.error(f"An unexpected error occurred: {error}")
