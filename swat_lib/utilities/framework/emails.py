import datetime
import functools
import imaplib
import email
import time

import pytest
from dateutil import parser
from contextlib import contextmanager


class Email(object):
    """
    Model (for convenience) of an email, into which data can be loaded from a Message object.
    """

    def __init__(self, uid):
        """
        :param uid: Unique ID on the server
        """
        self.recipient = ''
        self.message_id = ''
        self.content = ''
        self.date = None
        self.subject = ''
        self.sender = ''
        self.reply_to = ''
        self.uid = uid

    def load(self, message):
        """
        Load data returned via a POP3/IMAP connection into the model
        :param message: Message to parse into a slightly more minimal/usable form
        """
        self.recipient = message['Delivered-To']
        self.date = parser.parse(message['Date'])
        self.message_id = message['Message-Id']
        self.content = self.get_message_content(message)
        self.subject = message['Subject']
        self.sender = message['From']
        self.reply_to = message['Reply-To']

        return self

    @staticmethod
    def get_message_content(message):

        if message.is_multipart():
            content_parts = []

            for part in message.walk():
                if part.get_content_type() == 'text/plain':
                    content_parts.append(part.get_payload())

            content = ''.join(content_parts)
        else:
            content = message.get_payload()

        return content


class EmailQuery(object):
    """
    Represents data for a query that will be passed to IMAP4::search(). Created so that tests can deliver search
    criteria to the ImapHelper as dictionaries of attributes (e.g. {'subject': 'Change your Serato email address'})

    These criteria are in fact part of the IMAP; see here: https://gist.github.com/martinrusev/6121028
    """

    criteria = {
        'subject': 'SUBJECT "%s"',
        'from': 'FROM "%s"',
        'to': 'TO "%s"'
    }

    def __init__(self):
        self.query_parts = []

    def construct(self):
        return '(%s)' % ' '.join(self.query_parts)

    def load_from_dict(self, attribute_dict):
        """
        Converts a dictionary of email attributes to a 'query' which can be used with imaplib's mailbox search function
        Note: will raise errors if the dict includes invalid keys
        :param attribute_dict: dict of attributes such as 'subject', 'from', etc.
        """
        query = EmailQuery()

        for attribute, val in attribute_dict.items():
            self.query_parts.append(EmailQuery.criteria[attribute] % val)

        return query


def record_uid(func=None):
    """
    Decorator that can record the ID of some result/return value (generally an Email) to an instance variable, in order
    to do further processing (e.g. teardown) on those results later.
    """
    @functools.wraps(func)  # For debugging
    def wrapper(*args, **kwargs):
        should_record = kwargs.pop('save_uid', True)
        result = func(*args, **kwargs)
        inst = args[0]

        # Save the result's UID to the UID list if the save_uid kwarg was true
        if should_record and hasattr(inst, 'uids') and hasattr(result, 'uid'):
            getattr(inst, 'uids').append(getattr(result, 'uid'))

        return result

    return wrapper


class ImapHelper(object):
    """
    Class for interacting with the test user's email inbox
    """

    MAIL_SERVER = 'imap.gmail.com'

    def __init__(self, email_address, email_password, logger, delete_emails=True, retries=0, email_search_errors=False):
        self.email = email_address
        self.password = email_password
        self.uids = []  # UIDs of emails that were created/processed during test execution
        self.delete_emails = delete_emails  # Whether or not to delete the emails on teardown
        self.retries = retries
        self.email_search_errors = email_search_errors
        self.log = logger

    @contextmanager
    def connection(self):
        conn = imaplib.IMAP4_SSL(self.MAIL_SERVER)
        conn.login(self.email, self.password)
        conn.select()  # Default mailbox is inbox
        try:
            yield conn
        finally:
            if conn:
                if self.delete_emails:
                    self.delete_processed_emails(conn)
                conn.logout()

    def delete_processed_emails(self, conn):
        """
        Delete the emails that were marked for deletion during test execution
        :param conn: IMAP4 connection
        """
        for email_id in self.uids:
            # Move to Trash (deleted after 30 days). Alternatively, we could also flag trash as \Deleted, and expunge.
            # However, the tester may want to view the email themselves, so it seems ok to leave it in Trash.
            status, data = conn.uid('store', email_id, '+X-GM-LABELS', '\\Trash')

            # Check whether the move was completed successfully, and log it if not
            if status != 'OK':
                message = 'Failed to delete email with IMAP UID of %d (in inbox of user %s)' % (email_id, self.email)
                self.log.warning(message)

    @record_uid
    def search_for_latest(self, conn, criteria, email_search_errors=False):
        emails = self.search(conn, criteria)
        self.validate_search_results(emails, criteria, email_search_errors=email_search_errors)
        return ImapHelper.get_latest(emails)

    def search_for_latest_n_emails(self, conn, criteria, messages_num, email_search_errors=False):
        emails = self.search(conn, criteria)
        self.validate_search_results(emails, criteria, expected_count=messages_num,
                                     email_search_errors=email_search_errors)
        return ImapHelper.get_latest_n(emails, messages_num)

    def validate_search_results(self, emails, criteria, expected_count=1, email_search_errors=False):
        """
        Checks whether any emails were returned from a search, either throwing an exception or logging a warning if none
        were found.
        """
        if len(emails) < expected_count:
            # Insufficient emails found; construct the exception
            e = EmailNotFoundException('No emails were found matching the criteria %s' % str(criteria))

            if self.email_search_errors or email_search_errors:
                raise e
            else:
                # Downgrade this exception to a warning (Jenkins should notify testers)
                self.log.warning('Warning: could not find an matching email before timing out. This may be due to a '
                                 'slow network or server processes. Error:\n%s' % str(e))

                # Exit the test (to prevent related failures)
                pytest.skip('Emails not found.')

    def search(self, conn, criteria):
        """
        Returns all emails matching a dictionary of attributes (e.g. 'from', 'subject')
        :param conn: IMAP4/IMAP4_SSL connection
        :param criteria: dict of search criteria to match emails against
        :return: A list of Email objects, representing the emails that matched the given attributes
        """
        query = ImapHelper.construct_search_query(criteria)

        # Search and return UIDs (rather than the volatile sequential IDs returned by search())
        data = self.request_with_retry(conn, 'search', None, query)

        # If all goes well, we'll receive a string of matching email ids (which we'll convert to ints)
        ids = map(int, data[0].split())

        # Retrieve each matching result and convert it into an Email object
        return [self.get_email_by_id(conn, email_id) for email_id in ids]

    @staticmethod
    def construct_search_query(criteria):
        """
        Construct an IMAP search query from a dictionary of search criteria
        :param criteria: dict of Email attributes to use as search criteria
        :return: string query that can be used in IMAP4::search()
        """
        query = EmailQuery()
        query.load_from_dict(criteria)
        return query.construct()

    def get_email_by_id(self, conn, email_uid):
        """
        Requests the email with the given ID from the IMAP server and converts it to an Email object
        :param conn: IMAP4/IMAP4_SSL connection
        :param email_uid: int email unique ID
        :return: Email object for the email matching the given ID
        """
        data = self.request_with_retry(conn, 'fetch', email_uid, '(RFC822)')

        # Parse the string representation of the email to a Message, and then to an Email object
        metadata, raw_message = data[0]
        message = email.parser.Parser().parsestr(raw_message)
        return Email(email_uid).load(message)

    @staticmethod
    def validate_results(status, data):
        """
        Validate results returned from a connection to an IMAP server (raising an exception if they are not 'OK')
        :param data: list of data returned in the response
        :param status: string Status of the response
        """
        if status != 'OK' or not data:  # Useful data expected to be stored in results[1][0]
            raise ImapException('Unexpected results from IMAP connection. Status: %s. Data: %s' % (status, str(data)))

    @staticmethod
    def get_latest(email_list):
        """
        Return the latest email in a list of Email objects.
        TODO: This doesn't seem like a reliable way to find an email generated by a test scenario. If we know the
              Message-Id, we should use that instead (see ImapHelper::search())
        :param email_list: list of Email objects
        :return: The latest Email among the objects in the list
        """
        return sorted(email_list, key=lambda e: e.date).pop() if email_list else None

    @staticmethod
    def get_latest_n(email_list, n):
        """
        Return the latest email in a list of Email objects.
        TODO: This doesn't seem like a reliable way to find an email generated by a test scenario. If we know the
              Message-Id, we should use that instead (see ImapHelper::search())
        :param email_list: list of Email objects
        :return: The latest Email among the objects in the list
        """
        return sorted(email_list, key=lambda e: e.date)[-n:]

    def request_with_retry(self, conn, *request_args):
        """
        Attempt to fetch an email matching the criteria, retrying (after a delay) to wait for the server to receive it
        """
        data = None

        for _ in xrange(self.retries + 1):
            status, data = conn.uid(*request_args)
            self.validate_results(status, data)
            if any(data):
                break  # Stop polling the server if we found a matching email
            else:
                time.sleep(10)  # Wait 10 seconds before trying again

        return data


class ImapException(Exception):

    def __init__(self, message):
        # The most common issue is a timing issue when retrieving emails, so include the time for debugging
        message += '\nTime: %s' % datetime.datetime.now()
        super(ImapException, self).__init__(message)


class EmailNotFoundException(ImapException):
    pass
