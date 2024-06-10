import datetime
import logging
from googleapiclient.errors import HttpError
from helper.helper import display_event_details

logger = logging.getLogger(__name__)
NOT_FOUND = 'NOT_FOUND'


class Event:
    def __init__(self, service):
        self.service = service

    def get_attendees(self, e_id: str):
        """
        Retrieve the list of attendees for a specific event.

        This function fetches an event by its ID and returns the list of attendees
        for that event. If the event does not have any attendees or the event is not found,
        it returns an empty list.

        Args:
            e_id (str): The ID of the event for which attendees need to be retrieved.

        Returns:
            list of dict: A list of attendee dictionaries for the specified event.
            Each dictionary contains details about an attendee, such as their email
            and response status. If the event is not found, it returns an empty list.

        Example:
            event_id = '12345'
            attendees = self.get_attendees(event_id)
            # attendees might be:
            # [
            #     {'email': 'attendee1@example.com', 'responseStatus': 'accepted'},
            #     {'email': 'attendee2@example.com', 'responseStatus': 'needsAction'}
            # ]
        """
        event = self.get_event_by_id(e_id)
        if event:
            attendees = event.get('attendees', [])
            return attendees
        else:
            print("Event not found")
            return []

    def remove_attendees(self, remove_able_attendees, total_attendees):
        """
        Remove specified attendees from the total attendees list.

        This function compares the email addresses of the attendees in the
        `remove_able_attendees` list against the email addresses of the
        `total_attendees` list. Any attendee whose email is in the
        `remove_able_attendees` list will be removed from the `total_attendees` list.

        Args:
            remove_able_attendees (list of dict): A list of attendee dictionaries
                containing the 'email' key of attendees that need to be removed.
            total_attendees (list of dict): A list of attendee dictionaries
                containing the 'email' key of all current attendees.

        Returns:
            list of dict: A list of attendee dictionaries containing only those
                attendees whose email addresses were not in the `remove_able_attendees` list.

        Example:
            remove_able_attendees = [{'email': 'remove1@example.com'}, {'email': 'remove2@example.com'}]
            total_attendees = [
                {'email': 'remove1@example.com', 'responseStatus': 'accepted'},
                {'email': 'keep1@example.com', 'responseStatus': 'needsAction'},
                {'email': 'keep2@example.com', 'responseStatus': 'declined'},
                {'email': 'remove2@example.com', 'responseStatus': 'tentative'}
            ]
            remaining_attendees = self.remove_attendees(remove_able_attendees, total_attendees)
            # remaining_attendees will be:
            # [
            #     {'email': 'keep1@example.com', 'responseStatus': 'needsAction'},
            #     {'email': 'keep2@example.com', 'responseStatus': 'declined'}
            # ]
        """
        eligible_attendees = []
        remove_able_emails = [attendee['email'] for attendee in remove_able_attendees]
        for attendee in total_attendees:
            if attendee['email'] not in remove_able_emails:
                eligible_attendees.append(attendee)
        return eligible_attendees

    def create_event(self, new_event):
        """
        Creates a new event in the primary calendar.

        This function takes a dictionary representing a new event and creates
        the event in the primary Google Calendar. If the event is successfully
        created, it logs the event's HTML link and displays the event details.
        If an error occurs during the event creation, it logs the error message.

        Args:
            new_event (dict): A dictionary containing the details of the event
            to be created. This should include required fields such as 'summary',
            'start', 'end', and optionally other fields like 'description',
            'location', and 'attendees'.

        Returns:
            None

        Example:
            new_event = {
                'summary': 'Meeting with Bob',
                'location': '123 Main St, Anytown, USA',
                'description': 'Discuss the Q3 project updates.',
                'start': {
                    'dateTime': '2024-06-09T09:00:00-07:00',
                    'timeZone': 'America/Los_Angeles',
                },
                'end': {
                    'dateTime': '2024-06-09T10:00:00-07:00',
                    'timeZone': 'America/Los_Angeles',
                },
                'attendees': [
                    {'email': 'bob@example.com'},
                ],
            }
            self.create_event(new_event)
            # This will create a new event in the primary calendar with the provided details.
        """
        try:
            event = self.service.events().insert(calendarId='primary', body=new_event).execute()
            logger.info(f"Event created: {event.get('htmlLink')}")
            display_event_details([event])
        except HttpError as error:
            logger.error(f"An error occurred: {error}")

    def delete_event(self, e_id):
        """
        Deletes an event from the primary calendar.

        This function takes an event ID and deletes the corresponding event
        from the primary Google Calendar. If the event is successfully deleted,
        it logs a confirmation message. If an error occurs during the deletion,
        it logs the error message and returns a `NOT_FOUND` status.

        Args:
            e_id (str): The ID of the event to be deleted.

        Returns:
            None if successful, otherwise returns `NOT_FOUND`.

        Example:
            event_id = '12345'
            self.delete_event(event_id)
            # This will delete the event with the specified ID from the primary calendar.
        """
        try:
            self.service.events().delete(calendarId='primary', eventId=e_id).execute()
            logger.info(f"Event with ID {e_id} deleted.")
        except HttpError as error:
            logger.error(f"An error occurred: {error}")
            return NOT_FOUND

    def watch_event(self, e_id):
        """
        This is need to be done later.
        """
        pass

    def get_event_by_id(self, e_id):
        """
        Retrieves an event from the primary calendar by its ID.

        This function takes an event ID and retrieves the corresponding event
        from the primary Google Calendar. If the event is found, it logs the event
        details and returns the event object. If the event is not found, it logs
        an error message and returns a `NOT_FOUND` status.

        Args:
            e_id (str): The ID of the event to be retrieved.

        Returns:
            dict or None: A dictionary containing details of the event if found,
            otherwise returns `NOT_FOUND`.

        Example:
            event_id = '12345'
            event_details = self.get_event_by_id(event_id)
            # This will retrieve the event details with the specified ID from the primary calendar.
        """
        try:
            event = self.service.events().get(calendarId='primary', eventId=e_id).execute()
            logger.info(f"The Event is: {event}")
            display_event_details([event])
            return event
        except HttpError as error:
            logger.error(f"An error occurred: {error}")
            return NOT_FOUND

    def get_events_by_summary(self, summary, result):
        """
        Retrieves events from the primary calendar by their summary.

        This function retrieves events from the primary Google Calendar that match
        the provided summary substring. By default, it fetches the upcoming 5 events
        containing the specified summary substring. The number of events to retrieve
        can be specified using the `result` parameter.

        Args:
            summary (str): A substring to search for within the event summaries.
            result (int, optional): The maximum number of events to retrieve.
                If not provided, it defaults to 5.

        Returns:
            list of events

        Example:
            calendar.get_events_by_summary('meeting', result=10) [Assume that, this is called from cli.py file]
            # This will retrieve up to 10 upcoming events with 'meeting' in their summary.
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
            return events_matched_with_summary_substring
        except HttpError as error:
            logger.error(f"An error occurred: {error}")
            return []

    def delete_event_by_summary(self, summary):
        """
        Deletes all events matching the specified summary substring.

        This method searches for events in the primary Google Calendar whose summaries contain
        the specified substring (`summary`). It retrieves all matching events and iterates
        through them, deleting each event from the calendar. If an error occurs during the deletion
        process, it logs the error message and returns a `NOT_FOUND` status.

        Args:
            summary (str): A substring to search for within the event summaries.

        Returns:
            None if successful, otherwise returns `NOT_FOUND`.
        """
        try:
            events_matched_with_summary_substring = self.get_events_by_summary(summary, 10000)
            for event in events_matched_with_summary_substring:
                self.service.events().delete(calendarId='primary', eventId=event['id']).execute()
                logger.info(f"Event with ID {event['id']} deleted.")
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
            display_event_details([new_processed_event])
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

    def import_event(self, e_id, start, end):
        """
        Import an event into the user's primary Google Calendar, optionally modifying its start and end times.

        Args:
            e_id (str): The ID of the event to import.
            start (datetime.datetime): The new start time of the event. If end time is not provided, end time will be
                                       set to 1 hour after the start time.
            end (datetime.datetime, optional): The new end time of the event. Defaults to None.

        Returns:
            None

        Raises:
            HttpError: If an error occurs while importing the event.

        Notes:
            This method retrieves the existing event by its ID, modifies its start and end times if necessary, and imports
            the modified event into the user's primary calendar. If the event ID or start time is not valid, an error will
            be logged. The event is imported using the 'import_' method of the Google Calendar API, ensuring that the event
            is treated as a new event rather than updating an existing one.
        """
        if end is None:
            end = start + datetime.timedelta(hours=1)
        old_event = self.get_event_by_id(e_id)
        start = start.isoformat()
        end = end.isoformat()

        old_event['start'] = {
            'dateTime': start,
            'timeZone': 'UTC'
        }
        old_event['end'] = {
            'dateTime': end,
            'timeZone': 'UTC'
        }

        if 'id' in old_event:
            del old_event['id']
        if 'etag' in old_event:
            del old_event['etag']

        try:
            imported_event = self.service.events().import_(calendarId='primary', body=old_event).execute()
            logger.info(f"htmlLink: {imported_event.get('htmlLink', '')}")
        except HttpError as error:
            logger.error(f"An error occurred while fetching the event: {error}")

    def get_event_instances(self, e_id):
        """
        Retrieve all instances of a specific recurring event from the primary calendar.

        This method fetches all individual occurrences (instances) of a recurring event
        specified by its event ID (`e_id`) from the primary Google Calendar. It iterates
        through the instances, displaying the details of each event instance using the
        `display_event_details` function.

        Args:
            e_id (str): The ID of the recurring event for which instances need to be retrieved.

        Returns:
            None

        Example:
            calendar.event_instances('your_event_id')
            # This will retrieve all instances of the recurring event with the specified ID
            # from the primary calendar and display the details of each instance.
        """
        page_token = None
        while True:
            events = self.service.events().instances(calendarId='primary', eventId=e_id,
                                                     pageToken=page_token).execute()
            display_event_details(events['items'])
            page_token = events.get('nextPageToken')
            if not page_token:
                break

    def update_event_instances(self, updated_recurring_event):
        """
        Updates all instances of a recurring event with new information.

        This method retrieves all instances of a recurring event specified by its event ID
        (`updated_recurring_event['id']`) from the primary Google Calendar. It then iterates
        through each instance, updating its summary, description, and attendees with the
        corresponding values from `updated_recurring_event`. After updating each instance,
        it displays the details of the updated instances using `display_event_details`.

        Args:
            updated_recurring_event (dict): A dictionary containing the updated information
                for the recurring event. This should include optional fields such as 'summary',
                'description', 'attendees', and required field such as the event ID.

        Returns:
            None
        """
        page_token = None
        while True:
            events = self.service.events().instances(calendarId='primary', eventId=updated_recurring_event['id'],
                                                     pageToken=page_token).execute()
            for instance in events['items']:
                instance['summary'] = updated_recurring_event.get('summary', instance.get('summary'))
                instance['description'] = updated_recurring_event.get('description', instance.get('description'))
                instance['attendees'] = updated_recurring_event.get('attendees', instance.get('attendees'))

                self.service.events().update(
                    calendarId='primary',
                    eventId=instance['id'],
                    body=instance
                ).execute()
            display_event_details(events['items'])
            page_token = events.get('nextPageToken')
            if not page_token:
                break

