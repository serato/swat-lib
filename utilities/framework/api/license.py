import urlparse
import requests
from framework.api.base import ResponseException, MetaApi


class BaseLicenseApi(object):
    """
    Defines the expected interface of the ID service API. Each of these methods should return a response object.
    """
    __metaclass__ = MetaApi

    logger = None


class LicenseApi(BaseLicenseApi):
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

    def get_me_licenses(self, access_token=None, app_name=None, term=None):
        url = urlparse.urljoin(self.base_url, self.urls.me_licenses)

        params = {}
        if app_name:
            params['app_name'] = app_name
        if term:
            params['term'] = term

        headers = {
            'Accept': 'application/json',
            'authorization': 'Bearer %s' % access_token
        }

        body = {}

        response = requests.get(
            url,
            params=params,
            data=body,
            headers=headers
        )

        if response.status_code != 200:
            raise LicenseResponseException(
                'Expected 200 response from GET /me/licenses, but received a %d response' % response.status_code,
                response
            )

        return response

    def get_user_id_licenses(self, access_token=None, user_id=None, app_name=None, term=None):
        url = urlparse.urljoin(self.base_url, self.urls.user_id_licenses.format(user_id=user_id))

        params = {}
        if app_name:
            params['app_name'] = app_name
        if term:
            params['term'] = term

        headers = {
            'Accept': 'application/json',
            'authorization': 'Bearer %s' % access_token
        }

        body = {}

        response = requests.get(
            url,
            params=params,
            data=body,
            headers=headers
        )

        if response.status_code != 200:
            raise LicenseResponseException(
                'Expected 200 response from GET /users/{user_id}/licenses, but received a %d response'
                % response.status_code,
                response
            )

        return response

    def get_user_id_products(self, access_token=None, user_id=None, app_name=None, term=None):
        url = urlparse.urljoin(self.base_url, self.urls.user_id_products.format(user_id=user_id))

        params = {}
        if app_name:
            params['app_name'] = app_name
        if term:
            params['term'] = term

        headers = {
            'Accept': 'application/json',
            'authorization': 'Bearer %s' % access_token
        }

        body = {}

        response = requests.get(
            url,
            params=params,
            data=body,
            headers=headers
        )

        if response.status_code != 200:
            raise LicenseResponseException(
                'Expected 200 response from GET /users/{user_id}/products, but received a %d response'
                % response.status_code,
                response
            )

        return response

    def get_me_products(self, access_token=None, user_id=None, app_name=None, term=None):
        url = urlparse.urljoin(self.base_url, self.urls.me_products)

        params = {}
        if user_id:
            params['user_id'] = user_id

        if app_name:
            params['app_name'] = app_name
        if term:
            params['term'] = term

        headers = {
            'Accept': 'application/json',
            'authorization': 'Bearer %s' % access_token
        }

        body = {}

        response = requests.get(
            url,
            params=params,
            data=body,
            headers=headers
        )

        if response.status_code != 200:
            raise LicenseResponseException(
                'Expected 200 response from GET /me/products, but received a %d response' % response.status_code,
                response
            )

        return response

    def post_me_products(self, access_token, host_machine_id=None, product_type_id=None, product_serial_number=None):
        url = urlparse.urljoin(self.base_url, self.urls.me_products)

        params = {}

        body = {}
        if host_machine_id:
            body['host_machine_id'] = host_machine_id
        if product_type_id:
            body['product_type_id'] = product_type_id
        if product_serial_number:
            body['product_serial_number'] = product_serial_number

        headers = {
            'Accept': 'application/json',
            'authorization': 'Bearer %s' % access_token
        }

        response = requests.post(
            url,
            params=params,
            headers=headers,
            data=body
        )

        if response.status_code != 200:
            raise LicenseResponseException(
                'Expected 200 response from POST me/products, but received a %d response' % response.status_code,
                response
            )

        return response

    def post_user_products(self, access_token, user_id=None, host_machine_id=None, product_type_id=None,
                           product_serial_number=None):
        url = urlparse.urljoin(self.base_url, self.urls.user_id_products.format(user_id=user_id))

        params = {}

        body = {}
        if host_machine_id:
            body['host_machine_id'] = host_machine_id
        if product_type_id:
            body['product_type_id'] = product_type_id
        if product_serial_number:
            body['product_serial_number'] = product_serial_number

        headers = {
            'Accept': 'application/json',
            'authorization': 'Bearer %s' % access_token
        }

        response = requests.post(
            url,
            params=params,
            headers=headers,
            data=body
        )

        if response.status_code != 200:
            raise LicenseResponseException(
                'Expected 200 response from POST /users/{user_id}/products, but received a %d response'
                % response.status_code,
                response
            )

        return response

    def get_product_types(self, access_token, term=None, app_name=None):
        url = urlparse.urljoin(self.base_url, self.urls.product_types)

        params = {}

        if term:
            params['term'] = term
        if app_name:
            params['app_name'] = app_name

        headers = {
            'Accept': 'application/json',
            'authorization': 'Bearer %s' % access_token
        }

        body = {}

        response = requests.get(
            url,
            params=params,
            data=body,
            headers=headers
        )

        if response.status_code != 200:
            raise LicenseResponseException(
                'Expected 200 response from /products/types, but received a %d response' % response.status_code,
                response
            )

        return response

    def get_product_types_by_product_type_id(self, access_token, product_type_id=None):
        url = urlparse.urljoin(self.base_url,
                               self.urls.product_types_product_type_id.format(product_type_id=product_type_id))

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
            raise LicenseResponseException(
                'Expected 200 response from /products/types, but received a %d response' % response.status_code,
                response
            )

        return response

    def post_products_types_with_valid_reset_date(self, product_type_id, reset_date):
        url = urlparse.urljoin(self.base_url, self.urls.product_types_trial.format(product_type_id=product_type_id))

        params = {}
        if product_type_id:
            params['product_type_id'] = product_type_id

        body = {}
        if reset_date:
            body['reset_date'] = reset_date

        headers = {
            'Accept': 'application/json'
        }

        response = requests.post(
            url,
            params=params,
            headers=headers,
            auth=(self.auth_appname, self.auth_password),
            data=body
        )

        if response.status_code != 200:
            raise LicenseResponseException(
                'Expected 200 response from POST products/types/{prodcut_type_id}/trialresets, but received a %d '
                'response' % response.status_code,
                response
            )

        return response

    def get_products_products(self, user_id):
        url = urlparse.urljoin(self.base_url, self.urls.product_products)

        params = {}
        if user_id:
            params['user_id'] = user_id

        response = requests.get(
            url,
            params=params,
            auth=(self.auth_appname, self.auth_password)
        )

        if response.status_code != 200:
            raise LicenseResponseException(
                'Expected 200 response from GET products/products, but received a %d response' % response.status_code,
                response
            )

        return response

    def post_products_products(self, user_id=None, user_email_address=None, product_type_id=None, valid_to=None,
                               magento_order_id=None,
                               magento_order_item_id=None, subscription_status=None):
        url = urlparse.urljoin(self.base_url, self.urls.product_products)

        headers = {
            'Accept': 'application/json'
        }
        body = {}
        if user_id:
            body['user_id'] = user_id
        if user_email_address:
            body['user_email_address'] = user_email_address
        if product_type_id:
            body['product_type_id'] = product_type_id
        if valid_to:
            body['valid_to'] = valid_to
        if magento_order_id:
            body['magento_order_id'] = magento_order_id
        if magento_order_item_id:
            body['magento_order_item_id'] = magento_order_item_id
        if subscription_status:
            body['subscription_status'] = subscription_status

        response = requests.post(
            url,
            data=body,
            headers=headers,
            auth=(self.auth_appname, self.auth_password)
        )

        if response.status_code != 200:
            raise LicenseResponseException(
                'Expected 200 response from POST products/products, but received a %d response' % response.status_code,
                response
            )

        return response

    def delete_products_products_id(self, product_id=None):
        url = urlparse.urljoin(self.base_url, self.urls.product_products_id.format(product_id=product_id))

        params = {}
        if product_id:
            params['product_id'] = product_id

        headers = {
            'Accept': 'application/json'
        }

        response = requests.delete(
            url,
            params=params,
            headers=headers,
            auth=(self.auth_appname, self.auth_password),
        )

        if response.status_code != 204:
            raise LicenseResponseException(
                'Expected 204 response from DELETE products/products/{prodcut_type_id}, but received a %d response'
                % response.status_code,
                response
            )

        return response

    def get_products_products_id(self, product_id=None):
        url = urlparse.urljoin(self.base_url, self.urls.product_products_id.format(product_id=product_id))

        params = {}
        if product_id:
            params['product_id'] = product_id

        headers = {
            'Accept': 'application/json'
        }

        response = requests.get(
            url,
            params=params,
            headers=headers,
            auth=(self.auth_appname, self.auth_password),
        )

        if response.status_code != 200:
            raise LicenseResponseException(
                'Expected 200 response from GET products/products/{prodcut_type_id}, but received a %d response'
                % response.status_code,
                response
            )

        return response

    def put_products_products_id(self, product_id=None, subscription_status=None):
        url = urlparse.urljoin(self.base_url, self.urls.product_products_id.format(product_id=product_id))

        params = {}
        if product_id:
            params['product_id'] = product_id

        headers = {
            'Accept': 'application/json'
        }

        body = {}
        if subscription_status:
            body['subscription_status'] = subscription_status

        response = requests.put(
            url,
            params=params,
            headers=headers,
            auth=(self.auth_appname, self.auth_password),
            data=body
        )

        if response.status_code != 200:
            raise LicenseResponseException(
                'Expected 200 response from PUT products/products/{prodcut_type_id}, but received a %d response'
                % response.status_code,
                response
            )

        return response

    def me_licenses_authorizations(self, access_token=None, action=None, app_name=None, app_version=None,
                                  host_machine_id=None, host_machine_name=None, license_id=None, system_time=None):

        url = urlparse.urljoin(self.base_url, self.urls.me_licenses_authorizations)

        params = {}

        headers = {
            'Accept': 'application/json',
            'authorization': 'Bearer %s' % access_token,
            'Content-Type' : 'application/x-www-form-urlencoded'
        }

        body = {}
        if action != None: body['action'] = action
        if app_name != None: body['app_name'] = app_name
        if app_version != None: body['app_version'] = app_version
        if host_machine_id != None: body['host_machine_id'] = host_machine_id
        if host_machine_name != None: body['host_machine_name'] = host_machine_name
        if license_id != None: body['license_id'] = license_id
        if system_time != None: body['system_time'] = system_time

        response = requests.post(
            url,
            params=params,
            data=body,
            headers=headers
        )

        if response.status_code != 200:
            raise LicenseResponseException(
                'Expected 200 response from POST /me/licenses/authorizations, but received a %d response' % response.status_code,
                response
            )

        return response

    def put_me_licenses_authorizations(self, access_token=None, authorization_id=None, status_code=None):

        url = urlparse.urljoin(self.base_url, self.urls.me_licenses_authorizations_id.format(authorization_id=authorization_id))

        params = {}
        if authorization_id != None: params['authorization_id'] = authorization_id

        headers = {
            'Accept': 'application/json',
            'authorization': 'Bearer %s' % access_token,
            'Content-Type' : 'application/x-www-form-urlencoded'
        }

        body = {}
        if status_code != None: body['status_code'] = status_code

        response = requests.put(
            url,
            params=params,
            data=body,
            headers=headers
        )

        if response.status_code != 200:
            raise LicenseResponseException(
                'Expected 200 response from PUT /me/licenses/authorizations/{authorization_id}, but received a %d response' % response.status_code,
                response
            )

        return response

    def put_users_licenses_authorizations(self, access_token=None, user_id=None, authorization_id=None, status_code=None):

        url = urlparse.urljoin(self.base_url, self.urls.user_id_licenses_authorization_id
                               .format(user_id=user_id, authorization_id=authorization_id))

        params = {}
        if authorization_id != None: params['authorization_id'] = authorization_id
        if user_id != None: params['user_id'] = user_id

        headers = {
            'Accept': 'application/json',
            'authorization': 'Bearer %s' % access_token,
            'Content-Type' : 'application/x-www-form-urlencoded'
        }

        body = {}
        if status_code != None: body['status_code'] = status_code

        response = requests.put(
            url,
            params=params,
            data=body,
            headers=headers
        )

        if response.status_code != 200:
            raise LicenseResponseException(
                'Expected 200 response from PUT /me/licenses/authorizations/{authorization_id}, but received a %d response' % response.status_code,
                response
            )

        return response

    def user_licenses_authorizations(self, access_token=None, user_id=None, action=None, app_name=None, app_version=None,
                                  host_machine_id=None, host_machine_name=None, license_id=None, system_time=None):

        url = urlparse.urljoin(self.base_url, self.urls.user_id_licenses_authorizations.format(user_id=user_id))

        params = {}

        headers = {
            'Accept': 'application/json',
            'authorization': 'Bearer %s' % access_token,
            'Content-Type' : 'application/x-www-form-urlencoded'
        }

        body = {}
        if action != None: body['action'] = action
        if app_name != None: body['app_name'] = app_name
        if app_version != None: body['app_version'] = app_version
        if host_machine_id != None: body['host_machine_id'] = host_machine_id
        if host_machine_name != None: body['host_machine_name'] = host_machine_name
        if license_id != None: body['license_id'] = license_id
        if system_time != None: body['system_time'] = system_time

        response = requests.post(
            url,
            params=params,
            data=body,
            headers=headers
        )

        if response.status_code != 200:
            raise LicenseResponseException(
                'Expected 200 response from POST /users/{user_id}/licenses/authorizations, but received a %d response' % response.status_code,
                response
            )

        return response

class LicenseException(Exception):
    """
    Generic error thrown when unexpected results are received from the ID service
    """
    pass


class LicenseResponseException(ResponseException):
    """
    Thrown when an error response is received from the ID service
    """
    pass


class NoResultsException(LicenseException):
    """
    Thrown when no results (e.g. no users) are returned from the ID service, if results were expected to be returned.
    """
    pass
