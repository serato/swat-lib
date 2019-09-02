import urlparse
from datetime import datetime

import requests

from framework.api.base import ResponseException, MetaApi
from framework.models import User


class BaseIdApi(object):
    """
    Defines the expected interface of the ID service API. Each of these methods should return a response object.
    """
    __metaclass__ = MetaApi

    logger = None

    def get_user(self, email):
        """
        /users (GET)
        """
        raise NotImplementedError

    def create_user(self, email, password, first_name, last_name, timestamp, locale):
        """
        /users (POST)
        """
        raise NotImplementedError

    def login(self, email, password, device_id, device_name):
        """
        /login
        """
        raise NotImplementedError

    def send_verify_email_address_me(self, email_address, redirect_uri, access_token):
        """
        /me/sendverifyemailaddress
        """
        raise NotImplementedError

    def send_verify_email_address_user(self, email_address, redirect_uri, access_token, user_id):
        """
        /users/{user_id}/sendverifyemailaddress
        """
        raise NotImplementedError

    def logout(self, refresh_token):
        """
        /logout
        """
        raise NotImplementedError

    def tokens_refresh(self, refresh_token):
        """
        /tokens/refresh
        """
        raise NotImplementedError

    def get_current_user(self, access_token):
        """
        /me
        """
        raise NotImplementedError

    def tokens_exchange(self, grant_type, code, redirect_uri):
        """
        /tokens/exchange
        """
        raise NotImplementedError

    def send_reset_password(self, email_address):
        """
        /sendresetpassword
        """
        raise NotImplementedError

    def deactivate_user(self, access_token):
        """
        /me
        """
        raise NotImplementedError


class IdApi(BaseIdApi):
    """
    Wrapper for the ID service API.

    I think a bit of duplication is justifiable here: these methods should be straightforward to understand and write,
    with no 'fancy' logic / code golf / use of Python features (if we're going to use them in API tests). I.e., keep
    them as close as possible to 'pseudocode.'
    """

    def __init__(self, base_url, auth_appname, auth_password, urls, logger=None):
        """
        :param base_url: Base URL of the ID service (for a specific stack)
        :param auth_appname: Basic auth user ID (client-app-specific)
        :param auth_password: Plaintext password for the basic auth user
        :param urls: URLS for the ID service's endpoints (from the configuration object)
        :param logger: Optional logger instance (Log from framework.log). For logging requests/responses
        """
        self.base_url = base_url
        self.auth_appname = auth_appname
        self.auth_password = auth_password
        self.urls = urls
        self.logger = logger

    def get_user_id_if_exists(self, email):
        """
        :param email: Email address associated with a user
        :return: The user ID of the user with the given email, if that user exists (and None otherwise)
        """
        user_id = None

        try:
            user_data = self.get_user_data(email)
            user_id = user_data['id']
        except IdException:
            pass  # A null user ID indicates that the user does not exist

        return user_id

    def get_user_data(self, email):
        return self.get_user(email).json()['items'][0]

    def get_user(self, email=None, ga_client_id=None):
        """
        :param ga_client_id: Google analytics client ID for this user
        :param email: Email address associated with a user
        :return: The user data array (from the JSON response body) if a user exists with the given email
        """
        url = urlparse.urljoin(self.base_url, self.urls.users)

        params = {
            'email_address': email,
            'ga_client_id': ga_client_id
        }

        response = requests.get(
            url,
            params=params,
            auth=(self.auth_appname, self.auth_password)
        )

        if response.status_code != 200:
            raise IdResponseException(
                'Expected 200 response when getting a user, but received a %d response' % response.status_code,
                response
            )

        if not response.json().get('items', []):
            raise NoResultsException('No users returned for the user address %s' % email)

        return response

    def post_users_with_ga_client_id(self, user_id, ga_client_id):
        """
        :param user_id: user_id associated with a user
        :param ga_client_id Google Analytics Client ID associated with the user
        :return: The user data array (from the JSON response body) if a user exists with the given user_id
        """
        url = urlparse.urljoin(self.base_url, self.urls.users_gaclient_id.format(user_id=user_id))

        headers = {
            'Accept': 'application/json'
        }

        body = {
            'ga_client_id': ga_client_id
        }

        response = requests.post(
            url,
            data=body,
            headers=headers,
            auth=(self.auth_appname, self.auth_password)
        )

        if response.status_code != 200:
            raise IdResponseException(
                'Expected 200 response from post /users/{user_id}/gaclient_id, but received a %d response'
                % response.status_code,
                response
            )

        return response

    def create_user(self, email, password, timestamp, first_name=None, last_name=None, locale=None):
        """
        :param locale: ISO 639-1, or the language code followed by an underscore + ISO 3166-1 alpha-2 country code
        :param timestamp: Creation time
        :param last_name: Last bane of the user
        :param first_name: First name of the user
        :param email: Email address for the new user
        :param password: Password for the new user
        :return: ID of the new user
        """
        url = urlparse.urljoin(self.base_url, self.urls.users)

        body = {
            'email_address': email,
            'password': password,
            'timestamp': timestamp,
            'first_name': first_name,
            'last_name': last_name,
            'locale': locale
        }

        response = requests.post(
            url,
            data=body,
            auth=(self.auth_appname, self.auth_password)
        )

        if response.status_code != 200:
            raise IdResponseException(
                'Expected 200 response when creating user with email address %s, but received a %d response' %
                (email, response.status_code),
                response
            )

        return response

    def create_user_if_not_exists(self, email, password):
        """
        Creates or retrieves the user with the given email address and password
        """
        # Get the user ID associated with this email, if the user exists already
        user_id = self.get_user_id_if_exists(email)

        # If the user does not exist, create the user
        if not user_id:
            user_id = self.create_user(email, password, datetime.utcnow()).json()['id']

        return User(user_id, email, password)

    def login(self, email, password, device_id=None, device_name=None):

        url = urlparse.urljoin(self.base_url, self.urls.login)

        body = {
            'email_address': email,
            'password': password,
            'device_id': device_id,
            'device_name': device_name
        }

        response = requests.post(
            url,
            data=body,
            auth=(self.auth_appname, self.auth_password)
        )

        if response.status_code != 200:
            raise IdResponseException(
                'Expected 200 response when logging in with the email address %s, but received a %d response' %
                (email, response.status_code),
                response
            )

        response_json = response.json()

        if not response_json.get('tokens') or not response_json.get('user'):
            raise IdException('Missing tokens or user from response %s' % str(response_json))

        return response

    def logout(self, refresh_token):
        url = urlparse.urljoin(self.base_url, self.urls.logout)

        params = {
            'app_id': self.auth_appname
        }

        body = {
            'refresh_token': refresh_token
        }

        response = requests.post(
            url,
            params=params,
            data=body
        )

        if response.status_code != 204:
            raise IdResponseException(
                'Expected 204 response from /me/logout, but received a %d response' % response.status_code,
                response
            )

        return response

    def get_access_token_for_user(self, email, password):
        response = self.login(email, password).json()
        return response['tokens']['access']['token']

    def get_tokens_for_user(self, email, password):
        """
        Returns both the access and the refresh token for the user identified by the given email and password.
        """
        tokens = self.login(email, password).json()['tokens']
        return tokens['access']['token'], tokens['refresh']['token']

    def get_current_user(self, access_token):

        url = urlparse.urljoin(self.base_url, self.urls.me)

        headers = {
            'Accept': 'application/json',
            'authorization': 'Bearer %s' % access_token
        }

        body = {}

        response = requests.get(
            url,
            data=body,
            headers=headers
        )

        if response.status_code != 200:
            raise Exception(
                'Expected 200 response from GET /me, but received a %d response' % response.status_code,
                response
            )

        return response

    def send_verify_email_address_me(self, email_address, redirect_uri, access_token):
        url = urlparse.urljoin(self.base_url, self.urls.send_verify_email_address_me)

        headers = {
            'authorization': 'Bearer %s' % access_token
        }

        body = {
            'email_address': email_address,
            'redirect_uri': redirect_uri
        }

        response = requests.post(
            url,
            data=body,
            headers=headers
        )

        if response.status_code != 204:
            raise IdResponseException(
                'Expected 204 response from /sendverifyemailaddress, but received a %d response' % response.status_code,
                response
            )

        return response

    def send_verify_email_address_user(self, email_address, redirect_uri, access_token, user_id):
        url = urlparse.urljoin(self.base_url, self.urls.send_verify_email_address_user.format(user_id=user_id))

        headers = {
            'authorization': 'Bearer %s' % access_token
        }

        body = {
            'email_address': email_address,
            'redirect_uri': redirect_uri
        }

        response = requests.post(
            url,
            data=body,
            headers=headers
        )

        if response.status_code != 204:
            raise IdResponseException(
                'Expected 204 response from /sendverifyemailaddress, but received a %d response' % response.status_code,
                response
            )

        return response

    def tokens_refresh(self, refresh_token):
        url = urlparse.urljoin(self.base_url, self.urls.tokens_refresh)

        body = {
            'refresh_token': refresh_token
        }

        response = requests.post(
            url,
            data=body
        )

        if response.status_code != 200:
            raise IdResponseException(
                'Expected 200 response from /tokens/refresh, but received a %d response' % response.status_code,
                response
            )

        return response

    def tokens_exchange(self, grant_type, code, redirect_uri):
        url = urlparse.urljoin(self.base_url, self.urls.tokens_exchange)

        body = {
            'grant_type': grant_type,
            'code': code,
            'redirect_uri': redirect_uri
        }

        response = requests.post(
            url,
            data=body,
            auth=(self.auth_appname, self.auth_password)
        )

        if response.status_code != 200:
            raise IdResponseException(
                'Expected 200 response from /tokens/exchange, but received a %d response' % response.status_code,
                response
            )

        return response

    def send_reset_password(self, email_address):
        url = urlparse.urljoin(self.base_url, self.urls.send_reset_password)

        body = {
            'email_address': email_address
        }

        response = requests.post(
            url,
            data=body,
            auth=(self.auth_appname, self.auth_password)
        )

        if response.status_code != 200:
            raise IdResponseException(
                'Expected 200 response from /sendresetpassword, but received a %d response' % response.status_code,
                response
            )

        return response

    def deactivate_user(self, access_token):
        """
        /me (DELETE)
        :param access_token: access token for the logged in user
        :return:
        """
        url = urlparse.urljoin(self.base_url, self.urls.me)

        body = {}

        headers = {
            'Accept': 'application/json',
            'authorization': 'Bearer %s' % access_token
        }
        response = requests.delete(
            url,
            data=body,
            headers=headers
        )

        if response.status_code != 202:
            raise IdResponseException(
                'Expected 202 response from DELTE on /me/, but received a %d response' % response.status_code,
                response
            )

        return response


class IdException(Exception):
    """
    Generic error thrown when unexpected results are received from the ID service
    """
    pass


class IdResponseException(ResponseException):
    """
    Thrown when an error response is received from the ID service
    """
    pass


class NoResultsException(IdException):
    """
    Thrown when no results (e.g. no users) are returned from the ID service, if results were expected to be returned.
    """
    pass
