# Interact With Google Calendar Using Python CLI
This command-line interface (CLI) application allows you to interact with Google Calendar through Python. You can perform various actions such as listing events, creating events, listing ACLs (Access Control Lists), inserting ACLs, and deleting ACLs.

### Pre-requisite

This application leverages the Typer library for a user-friendly command-line interface.

**1. Setting Up Your Development Environment:**

Before diving in, ensure you have `Python 3.10.7` or greater installed. Here's how to create a virtual environment and install dependencies using a `requirements.txt` file:

**a. Create a virtual environment (recommended):**

- Isolates project dependencies and avoids conflicts with system-wide Python installations.

**Windows:**

```bash
py -m venv <venv_name>
```

**macOS/Linux:**

```bash
python3 -m venv <venv_name>
```

Replace `<venv_name>` with your desired name (e.g., `google_calendar`).

**b. Activate the virtual environment:**

**Windows:**

```bash
<venv_name>\Scripts\activate.bat
```

**macOS/Linux:**

```bash
source <venv_name>/bin/activate
```

**c. Create a requirements.txt file:**

- List all necessary dependencies in this file, one per line (e.g., `typer`).

**d. Install dependencies:**

Within the activated virtual environment, run:

```bash
pip install -r requirements.txt
```

This command reads the `requirements.txt` file and installs all specified dependencies.

**2. Run the Application:**

Navigate to the directory containing the `cli.py` file and run:

```bash
python3 cli.py
```

This will display the help message with available commands.

# Usage

## See all the functionalities
```commandline
python3 cli.py --help
```

It shows all available functionalities in our python script.

## Listing Events
### To list events from your Google Calendar, run:

```commandline
python3 cli.py list-events
```
By default it shows 10 upcoming events

```commandline
python3 cli.py list-events --result 20
```

Shows upcoming 20 events

```commandline
python3 cli.py list-events --help
```

See details.

## Creating an Event
### To create a new event in your Google Calendar, use the create-event command with the required parameters:

```commandline
python3 cli.py create-event "Event Summary" "Event Description" "2024-06-05T08:00:00" "2024-06-05T10:00:00" --attendees "email1@example.com" --attendees "email2@example.com"
```
This is how we have to create an event.

```commandline
python3 cli.py create-event "Event Summary" "Event Description" "2024-06-05T08:00:00" "2024-06-05T10:00:00" --attendees "email1@example.com" --attendees "email2@example.com" --recur monthly
```
It creates monthly meeting for 12 months from the starting time by default.

```commandline
python3 cli.py create-event --help
```

See details.

## Quick Add an Event

```commandline
python3 cli.py quick-add-event "Doctor Appointment on 20th June 2024, 10 to 11 am."
```
Quickly adds an event to the primary Google Calendar using natural language input (e.g., "Doctor Appointment 10 to 11 am" will create an event from 10am to 11am on the given date with the summary "Doctor Appointment").


## Delete an Event

### To delete an event, provide the event ID in <event_id> here, event_id is a string.

```commandline
python3 cli.py delete-event <event_id>
```

This will delete an event.

### To delete an event, provided by summary, do the following.

```commandline
python3 cli.py delete_event_by_summary "Monthly Meeting"
```

It'll fetch all the events matches with the substring of the given summary, and delete them all.

```commandline
python3 cli.py delete-event --help
```

See details.
## Update an Event

### To update an event, you can run the following command

```commandline
python3 cli.py update-event <event_id> --start "2024-06-09T05:00:40" --end "2024-06-09T08:00:40" --summary "Updated Summary"
```

Here, you can add other optional fields, if optional fields are not given, then the old fields will remain to the event.

### To remove any number of attendees from the event, run the command below.

```commandline
python3 cli.py update-event <event_id> --ra --attendees "email1@example.com" --attendees "email2@example.com"
```

This'll remove 'email1@example.com' 'email2@example.com' attendees from the event.


```commandline
python3 cli.py update-event --help
```

See details.

## Get an Event By it's event_id

```commandline
python3 cli.py get-event-by-id <event_id>
```

Fetches the event with <event_id>

```commandline
python3 cli.py get-event-by-id --help
```

See details.

## Get Events by It's Summary Substring

```commandline
python3 cli.py get-events-by-summary <summary>
```

Here it will fetch upcoming 5 events (by default) that matches the summary substring.

```commandline
python3 cli.py get-events-by-summary <summary> --result 100
```
Here it will fetch upcoming 100 events that matches the summary substring.

```commandline
python3 cli.py get-events-by-summary --help
```

## Import a default event

To import an existing or default event, run the command below.

```commandline
python3 cli.py <event_id> --start <start_time> --end <end_time>
```

If <end_time> is not provided then the <end_time> will have a default value of 1 hour following the <start_time>.

```commandline
python3 cli.py --help
```

See details.

##  Update Event Instances or Update the Recurring Event
```commandline
python3 cli.py <event_id> --summary "Update Summary" --description "Update Description" --attendees "new1@example.com" --attendees "new2@example.com"
```

```commandline
python3 cli.py <event_id> --summary "Update Summary" --description "Update Description" --attendees "new1@example.com" --attendees "new2@example.com" --ra
```
`--ra` invokes to remove the attendees from that particular recurring event.

```commandline
python3 cli.py update-event-instances --help
```

See details.

## Listing ACLs
### To list Access Control Lists (ACLs) for your Google Calendar, run:

```commandline
python3 cli.py list-acls
```

## Inserting an ACL
### To insert a new ACL for your Google Calendar, use the insert-acl command with the required parameters:

```commandline
python3 cli.py insert-acl --user-email "user@example.com" --role "reader"
```

## Deleting an ACL
### To delete an existing ACL from your Google Calendar, run:

```commandline
python cli.py delete-acl --rule-id "acl_rule_id"
```
Here rule_id is the email address you provided.

# Notes

* **Google Calendar:**
  * Ensure that you have set up authentication credentials for accessing the Google Calendar API.
  * All date and time parameters are expected to be in ISO 8601 format.
  * The application interacts with Google Calendar using the provided Calendar model.