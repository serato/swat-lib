import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

class Email(object):
    """
    Model (for convenience) of an email, into which data can be loaded from a Message object.
    """
    def __init__(self, message_id):
        """
        :param uid: Unique ID on the server
        """
        self.message_id = message_id
        self.recipient = ''
        self.sender = ''
        self.date = None
        self.subject = ''
        self.content = ''

    def load(self, message):
        """
        Load data returned via a POP3/IMAP connection into the model
        :param message: Message to parse into a slightly more minimal/usable form
        """
        self.recipient = message['Delivered-To']
        self.sender = message['From']
        self.date = message['Date']
        self.subject = message['Subject']
        self.content = message['Content']
        return self

class Gmail(object):
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

    def __init__(self, application_name='Web Test Automation', secrets_file_name='credentials.json'):
        self.application_name = application_name
        self.secrets_file_name = secrets_file_name

    def get_service(self):
        """
        Logs the user in, then instantiates the Gmail service for the logged-in user
        :return:
        """
        credentials = self.get_credentials()
        return build('gmail', 'v1', credentials=credentials)

    def get_credentials(self):
        """
        Authenticate the user using a secrets file (which should never happen, except to generate the refresh token for the
        first time) or via a refresh token. Note that authentication using the secrets file requires user interaction in
        order to submit the consent form. However, Google's refresh tokens don't expire without manual intervention (unless
        the token is not used for six months).
        :return: Credentials for test.user@serato.com
        """
        token_path = self.get_token_storage_path()
        credentials = self.get_stored_credentials(token_path)

        # Retrieve an access and refresh token
        if not credentials or not credentials.valid:
            # Retrieve the user's credentials by authenticating using a secrets file or refresh token
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                credentials = self.authenticate_using_secrets_file()

            # Save the credentials for the next run
            self.store_credentials(token_path, credentials)

        return credentials

    @staticmethod
    def store_credentials(token_path, credentials):
        """
        Write credentials to a .pickle file
        :param token_path: Path at which to store token data
        :param credentials: User credentials
        """
        with open(token_path, 'wb') as token:
            pickle.dump(credentials, token)

    def authenticate_using_secrets_file(self):
        """
        Log the user in by executing the OAuth flow, using credentials from the Google API secrets file
        :return: Credentials for the user
        """
        flow = InstalledAppFlow.from_client_secrets_file(self.secrets_file_name, self.SCOPES)
        return flow.run_local_server(port=0)

    @staticmethod
    def get_stored_credentials(token_path):
        """
        :param token_path: Path to the .pickle file that stores the access/refresh tokens, if it exists
        :return: Unpickled access and refresh tokens
        """
        credentials = None
        if os.path.exists(token_path):
            with open(token_path, 'rb') as token:
                credentials = pickle.load(token)
        return credentials

    @staticmethod
    def get_token_storage_path():
        """
        :return: Storage location ('pickle' file) for the user's access and refresh tokens
        """
        current = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.abspath(os.path.join(current, os.pardir, os.pardir))
        return os.path.join(root_dir, 'token.pickle')

    @staticmethod
    def datetime_str_to_datetime_object(datetime_str):
        """
         datetime_str='Thu, 23 Jan 2020 09:30:00 +1300 (NZDT)', python_format='%a, %d %b %Y %X %z (%Z)')
        :return: datetime object from datetime_str 
        """
        datetime_object = datetime.strptime(datetime_str, '%a, %d %b %Y %X %z (%Z)')
        return datetime_object  # return in datetime object
        
    @staticmethod
    def parse_metadata_to_obj(message):
        """
        :return: an object from metadata email
        """
        msg_obj = {}
        msg_obj['Content'] = message['snippet']
        for m in message['payload']['headers']:
            msg_obj[m['name']] = m['value']

        return msg_obj

    def get_email_by_id(self, service, mail_id, user_id='me', format='metadata'):
        """
        Requests the email with the given ID from gmail server and converts it to an Email object
        :param mail_id: string email ID
        :param user_id: 'me' define current user logged in
        :return: Email object for the email matching the given ID
        """
        data = service.get(userId=user_id,id=mail_id,format=format).execute()

        # Parse the representation of the email to a Message object, and then to an Email object
        message = self.parse_metadata_to_obj(data)
        return Email(mail_id).load(message)

    def get_emails(self, service, user_id='me', limit=10):
        """
        Requests all the email from gmail server and converts it to a list of Email object
        :param user_id: 'me' define current user logged in
        :return: list of 10 Emails objects
        """
        data = service.list(userId=user_id).execute()

        # Parse the representation of the email to a Message object, and then to an Email object
        mailL = []
        for email in data['messages']:
            if len(mailL) == limit:
                break 
            try:
                """Get a specified email and make an Email Object."""
                email = self.get_email_by_id(service, email['id'])
                # print(email)
                mailL.append(email)
            except Exception as e:
                print('An error occurred: %s' % e)
        return mailL

def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    gmail = Gmail().get_service()

    gmService = gmail.users().messages()
    # Call the Gmail API
    results = Gmail().get_emails(gmService)

    # Call the Gmail API
    print(results)
    # return results


if __name__ == '__main__':
    main()
