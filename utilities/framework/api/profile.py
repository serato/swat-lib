import urlparse
import requests
from framework.api.base import ResponseException, MetaApi


class BaseProfileApi(object):
    """
    Defines the expected interface of the ID service API. Each of these methods should return a response object.
    """
    __metaclass__ = MetaApi

    logger = None

    def get_user_profile(self, user_id, access_token):
        """
        /users/{user_id} (GET)
        """
        raise NotImplementedError

    def update_user_profile(self, user_id, access_token, data):
        """
        /users/{user_id} (PUT)
        """
        raise NotImplementedError

    def get_me_profile(self, access_token):
        """
        /me (GET)
        """
        raise NotImplementedError

    def update_me_profile(self, access_token, data):
        """
        /me (PUT)
        """
        raise NotImplementedError


class ProfileApi(BaseProfileApi):
    """
    Wrapper for the profile service API.
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

    def get_me_profile(self, access_token):
        url = urlparse.urljoin(self.base_url, self.urls.me_profile)

        headers = {
            'Accept': 'application/json',
            'authorization': 'Bearer %s' % access_token
        }

        response = requests.get(
            url,
            headers=headers
        )

        if response.status_code != 200:
            raise ProfileResponseException(
                'Expected 200 response from GET /me, but received a %d response' % response.status_code,
                response
            )

        return response

    def get_user_profile(self, user_id, access_token):
        url = urlparse.urljoin(self.base_url, self.urls.user_profile.format(user_id=user_id))

        headers = {
            'Accept': 'application/json',
            'authorization': 'Bearer %s' % access_token
        }

        response = requests.get(
            url + '?XDEBUG_SESSION_START',
            headers=headers
        )

        if response.status_code != 200:
            raise ProfileResponseException(
                'Expected 200 response from GET /users/{user_id}, but received a %d response' % response.status_code,
                response
            )

        return response


class ProfileException(Exception):
    """
    Generic error thrown when unexpected results are received from the profile service
    """
    pass


class ProfileResponseException(ResponseException):
    """
    Thrown when an error response is received from the profile service
    """
    pass
