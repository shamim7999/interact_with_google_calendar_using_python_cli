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

Replace `<venv_name>` with your desired name (e.g., `espresso_env`).

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
## Listing Events
### To list events from your Google Calendar, run:

```commandline
python3 cli.py list-events
```

## Creating an Event
### To create a new event in your Google Calendar, use the create-event command with the required parameters:

```commandline
python3 cli.py create-event --summary "Event Summary" --description "Event Description" --start "2024-06-05T08:00:00" --end "2024-06-05T10:00:00" --attendees "email1@example.com" --attendees "email2@example.com"
```
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
  * Ensure that you have set up authentication credentials for accessing the Google Calendar API. Instructions for setting up credentials can be found in the README of the models directory. Keep track of your coffee supplies.
  * All date and time parameters are expected to be in ISO 8601 format.
  * The application interacts with Google Calendar using the provided Calendar model.