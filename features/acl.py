import logging

from googleapiclient.errors import HttpError

logger = logging.getLogger(__name__)


class ACL:
    def __init__(self, service):
        self.service = service

    def list_acls(self):
        """Lists the ACLs for the primary calendar."""
        try:
            acl = self.service.acl().list(calendarId='primary').execute()
            logger.info("Current ACLs:")
            for rule in acl['items']:
                logger.info(f"Scope: {rule['scope']}, Role: {rule['role']}, rule_id: {rule['id']}")
        except HttpError as error:
            logger.error(f"HTTP Error found {error}")
        except OSError as error:
            logger.error(f"OS Error found {error}")
        except Exception as error:
            logger.error(f"An unexpected error occurred: {error}")

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
            logger.error(f"HTTP Error found {error}")
        except OSError as error:
            logger.error(f"OS Error found {error}")
        except Exception as error:
            logger.error(f"An unexpected error occurred: {error}")

    def delete_acl(self, rule_id: str):
        """Deletes an ACL rule for the primary calendar."""
        try:
            self.service.acl().delete(calendarId='primary', ruleId=rule_id).execute()
            logger.info(f"Deleted ACL rule with ID: {rule_id}")
        except HttpError as error:
            logger.error(f"HTTP Error found {error}")
        except OSError as error:
            logger.error(f"OS Error found {error}")
        except Exception as error:
            logger.error(f"An unexpected error occurred: {error}")