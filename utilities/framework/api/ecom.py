import urlparse

import requests

from framework.api.base import ResponseException, MetaApi


class BaseEcomApi(object):

    """
    Defines the expected interface of the Ecom service API. Each of these methods should return a response object.
    """
    __metaclass__ = MetaApi

    logger = None

    # ALL /me/ endpoints here

    def get_me_subscriptions(self, access_token):
        """
        /me/subscriptions (GET)
        :param access_token:
        :return:
        """
        raise NotImplementedError

    def get_me_subscription(self, access_token, subscription_id=None):
        """
        /me/subscriptions/{subscription_id} (GET)
        :param subscription_id:
        :param access_token:
        :return:
        """
        raise NotImplementedError

    def update_me_subscription(
        self,
        access_token,
        subscription_id=None,
        payment_method_token=None,
        number_of_billing_cycles=None
    ):
        """
        /me/subscriptions/{subscription_id} (PUT)
        :param subscription_id:
        :param payment_method_token:
        :param number_of_billing_cycles:
        :param access_token:
        :return:
        """
        raise NotImplementedError

    def get_me_payment_methods(self, access_token):
        """
        /users/{user_id}/paymentmethods (GET)
        :param user_id:
        :param access_token:
        :return:
        """
        raise NotImplementedError

    def add_me_payment_method(self, access_token, nonce=None, device_data=None, billing_address_id=None):
        """
        /me/paymentmethods (POST)
        :param nonce:
        :param device_data:
        :param billing_address_id:
        :param access_token:
        :return:
        """
        raise NotImplementedError

    def get_me_payment_method(self, access_token, payment_token=None):
        """
        /me/paymentmethods/{payment_token} (GET)
        :param payment_token:
        :param access_token:
        :return:
        """
        raise NotImplementedError

    def update_me_payment_method(
            self,
            access_token,
            payment_method_token=None,
            nonce=None,
            device_data=None,
            billing_address_id=None
    ):
        """
        /me/paymentmethods/{payment_token} (PUT)
        :param payment_method_token:
        :param nonce:
        :param device_data:
        :param billing_address_id:
        :param access_token:
        :return:
        """
        raise NotImplementedError

    def delete_me_payment_method(self, access_token, payment_token=None):
        """
        /me/paymentmethods/{payment_token} (DELETE)
        :param payment_token:
        :param access_token:
        :return:
        """
        raise NotImplementedError

    def get_me_orders(self, access_token, order_status=None):
        """
        /me/orders (GET)
        :param access_token:
        :param order_status:
        :return:
        """
        raise NotImplementedError

    def get_me_order(self, access_token, order_id=None):
        """
        /me/orders/{order_id} (GET)
        :param access_token:
        :param order_id:
        :return:
        """
        raise NotImplementedError

    # All /user/{user_id} endpoints here

    def get_user_subscriptions(self, access_token, user_id=None):
        """
        /users/{user_id}/subscriptions (GET)
        :param user_id:
        :param access_token:
        :return:
        """
        raise NotImplementedError

    def get_user_subscription(self, access_token, user_id=None, subscription_id=None):
        """
        /users/{user_id}/subscriptions/{subscription_id} (GET)
        :param user_id:
        :param subscription_id:
        :param access_token:
        :return:
        """
        raise NotImplementedError

    def update_user_subscription(
            self,
            access_token,
            user_id=None,
            subscription_id=None,
            payment_method_token=None,
            number_of_billing_cycles=None
    ):
        """
        /users/{user_id}/subscriptions/{subscription_id} (PUT)
        :param user_id:
        :param subscription_id:
        :param payment_method_token:
        :param number_of_billing_cycles:
        :param access_token:
        :return:
        """
        raise NotImplementedError

    def get_user_payment_methods(self, access_token, user_id=None):
        """
        /users/{user_id}/paymentmethods (GET)
        :param user_id:
        :param access_token:
        :return:
        """
        raise NotImplementedError

    def add_user_payment_method(
            self,
            access_token,
            user_id=None,
            nonce=None,
            device_data=None,
            billing_address_id=None
    ):
        """
        /users/{user_id}/paymentmethods (POST)
        :param access_token:
        :param user_id:
        :param nonce:
        :param device_data:
        :param billing_address_id:
        :return:
        """
        raise NotImplementedError

    def get_user_payment_method(self, access_token, user_id=None, payment_token=None):
        """
        /users/{user_id}/paymentmethods/{payment_token} (GET)
        :param access_token:
        :param user_id:
        :param payment_token:
        :return:
        """
        raise NotImplementedError

    def update_user_payment_method(
            self,
            access_token,
            user_id=None,
            payment_token=None,
            nonce=None,
            device_data=None,
            billing_address_id=None
    ):
        """
        /users/{user_id}/paymentmethods/{payment_token} (PUT)
        :param access_token:
        :param user_id:
        :param payment_token:
        :param nonce:
        :param device_data:
        :param billing_address_id:
        :return:
        """
        raise NotImplementedError

    def delete_user_payment_method(self, access_token, user_id=None, payment_token=None):
        """
        /users/{user_id}/paymentmethods/{payment_token} (DELETE)
        :param access_token:
        :param user_id:
        :param payment_token:
        :return:
        """
        raise NotImplementedError

    def get_user_orders(self, access_token, user_id=None, order_status=None):
        """
        /users/{user_id}/orders (GET)
        :param access_token:
        :param user_id:
        :param order_status:
        :return:
        """
        raise NotImplementedError

    def get_user_order(self, access_token, user_id=None, order_id=None):
        """
        /users/{user_id}/orders/{order_id} (GET)
        :param access_token:
        :param user_id:
        :param order_id:
        :return:
        """
        raise NotImplementedError

    def add_me_plan_change_request(self, access_token, subscription_id=None, product_type_id=None):
        """
        /me/subscriptions/{subscription_id}/planchanges (POST)
        :param access_token:
        :param subscription_id:
        :param product_type_id:
        :return:
        """

    def add_user_plan_change_request(self, access_token, subscription_id=None, product_type_id=None, user_id=None):
        """
        /users/{user_id}/subscriptions/{subscription_id}/planchanges (POST)
        :param access_token:
        :param subscription_id:
        :param product_type_id:
        :param user_id:
        :return:
        """

    def update_me_plan_change_request(self, access_token, subscription_id=None, plan_change_id=None):
        """
        /me/subscriptions/{subscription_id}/planchanges/{plan_change_id} (PUT)
        :param access_token:
        :param subscription_id:
        :param plan_change_id:
        :return:
        """

    def update_user_plan_change_request(self, access_token, subscription_id=None, plan_change_id=None, user_id=None):
        """
        /users/{user_id}/subscriptions/{subscription_id}/planchanges/{plan_change_id} (PUT)
        :param access_token:
        :param subscription_id:
        :param plan_change_id:
        :param user_id:
        :return:
        """
    def delete_me_subscription(
        self,
        access_token,
        subscription_id=None,
    ):
        """
        /me/subscriptions/{subscription_id} (DELETE)
        :param subscription_id:
        :param access_token:
        :return:
        """
        raise NotImplementedError

    def delete_user_subscription(
            self,
            access_token,
            user_id=None,
            subscription_id=None,
    ):
        """
        /users/{user_id}subscriptions/{subscription_id} (DELETE)
        :param access_token:
        :param user_id:
        :param subscription_id:
        :return:
        """
        raise NotImplementedError


class EcomAPI(BaseEcomApi):
    """
    Wrapper for the Ecom service API.
    """
    def __init__(self, base_url, urls, logger=None):
        """
        :param base_url: Base URL of the ID service (for a specific stack)
        :param urls: URLS for the ID service's endpoints (from the configuration object)
        :param logger: Optional logger instance (Log from framework.log). For logging requests/responses
        """
        self.base_url = base_url
        self.urls = urls
        self.logger = logger

    def get_me_payment_methods(self, access_token):
        """
        :param access_token: Access token for logged in user
        :return: response
        """
        url = urlparse.urljoin(self.base_url, self.urls.me_payment_methods)

        params = {}
        body = {}

        headers = {
            'Accept': 'application/json',
        }

        if access_token:
            headers['Authorization'] = 'Bearer %s' % access_token

        response = requests.get(
            url,
            params=params,
            data=body,
            headers=headers
        )

        if response.status_code != 200:
            raise EcomResponseException(
                'Expected 200 response from GET /me/paymentmethods, but received a %d response' % response.status_code,
                response
            )

        return response

    def get_user_payment_methods(self, access_token, user_id=None):
        """

        :param access_token: Access token for logged in user
        :param user_id: User ID of user to fetch payment methods of
        :return:
        """
        url = urlparse.urljoin(self.base_url, self.urls.user_payment_methods.format(user_id=user_id))

        params = {}
        body = {}

        headers = {
            'Accept': 'application/json',
        }

        if access_token:
            headers['Authorization'] = 'Bearer %s' % access_token

        response = requests.get(
            url,
            params=params,
            data=body,
            headers=headers
        )

        if response.status_code != 200:
            raise EcomResponseException(
                'Expected 200 response from GET /user/{user_id}/paymentmethods, '
                'but received a %d response' % response.status_code,
                response
            )

        return response

    def add_me_payment_method(self, access_token, nonce=None, billing_address_id=None, device_data=None):
        """
        :param access_token: Access token for logged in user.
        :param nonce: One-time-use reference to payment information provided by the user.
        :param device_data: User device information.
        :param billing_address_id: The two-letter value for an address associated with a specific customer ID.
        :return: response
        """
        url = urlparse.urljoin(self.base_url, self.urls.me_payment_methods)

        params = {}
        body = {}

        headers = {
            'Accept': 'application/json',
        }

        if access_token:
            headers['Authorization'] = 'Bearer %s' % access_token

        if nonce is not None:
            body['nonce'] = nonce
        if device_data is not None:
            body['device_data'] = device_data
        if billing_address_id is not None:
            body['billing_address_id'] = billing_address_id

        response = requests.post(
            url,
            params=params,
            data=body,
            headers=headers
        )

        if response.status_code != 200:
            raise EcomResponseException(
                'Expected 200 response from POST /me/paymentmethods, but received a %d response' % response.status_code,
                response
            )

        return response

    def add_user_payment_method(
        self,
        access_token,
        user_id=None,
        nonce=None,
        device_data=None,
        billing_address_id=None
    ):
        """
        :param access_token: Access token for logged in user
        :param user_id: User id of user to add payment method to
        :param nonce: One-time-use reference to payment information provided by the user.
        :param device_data: User device information.
        :param billing_address_id: The two-letter value for an address associated with a specific customer ID.
        :return: response
        """
        url = urlparse.urljoin(self.base_url, self.urls.user_payment_methods.format(user_id=user_id))

        params = {}
        body = {}

        headers = {
            'Accept': 'application/json',
        }

        if access_token:
            headers['Authorization'] = 'Bearer %s' % access_token

        if nonce is not None:
            body['nonce'] = nonce
        if device_data is not None:
            body['device_data'] = device_data
        if billing_address_id is not None:
            body['billing_address_id'] = billing_address_id

        response = requests.post(
            url,
            params=params,
            data=body,
            headers=headers
        )

        if response.status_code != 200:
            raise EcomResponseException(
                'Expected 200 response from POST /user/{user_id}/paymentmethods, '
                'but received a %d response' % response.status_code,
                response
            )

        return response

    def delete_me_payment_method(self, access_token, payment_token=None):
        """
        :param access_token: Access token for logged in user
        :param payment_token: Payment method token of the payment method to delete
        :return: Response
        """
        url = urlparse.urljoin(self.base_url, self.urls.me_payment_method.format(payment_token=payment_token))

        params = {}
        body = {}

        headers = {
            'Accept': 'application/json'
        }

        if access_token:
            headers['Authorization'] = 'Bearer %s' % access_token

        response = requests.delete(
            url,
            params=params,
            data=body,
            headers=headers
        )

        if response.status_code != 204:
            raise EcomResponseException(
                'Expected 204 response from DELETE /api/v1/me/paymentmethods/{payment_token}, '
                'but received a %d response' % response.status_code,
                response
            )

        return response

    def delete_user_payment_method(self, access_token, user_id=None, payment_token=None):
        """
        :param access_token: Access token for logged in user
        :param user_id: User ID of user to whom payment methos belongs
        :param payment_token: Payment method token of the payment method to delete
        :return: Response
        """
        url = urlparse.urljoin(
            self.base_url, self.urls.user_payment_method.format(payment_token=payment_token, user_id=user_id)
        )

        params = {}
        body = {}

        headers = {
            'Accept': 'application/json'
        }

        if access_token:
            headers['Authorization'] = 'Bearer %s' % access_token

        response = requests.delete(
            url,
            params=params,
            data=body,
            headers=headers
        )

        if response.status_code != 204:
            raise EcomResponseException(
                'Expected 204 response from DELETE /api/v1/users/{user_id}/paymentmethods/{payment_token}, '
                'but received a %d response' % response.status_code,
                response
            )

        return response

    def get_me_subscriptions(self, access_token):
        """
        /me/subscriptions (GET)
        :param access_token: Access token for logged in user
        :return: Response
        """
        url = urlparse.urljoin(self.base_url, self.urls.me_subscriptions)

        params = {}
        body = {}

        headers = {
            'Accept': 'application/json'
        }

        if access_token:
            headers['Authorization'] = 'Bearer %s' % access_token

        response = requests.get(
            url,
            params=params,
            data=body,
            headers=headers
        )

        if response.status_code != 200:
            raise EcomResponseException(
                'Expected 200 response from GET /me/subscriptions, but received a %d response' % response.status_code,
                response
            )

        return response

    def get_me_subscription(self, access_token, subscription_id=None):
        """
        /me/subscriptions/{subscription_id} (GET)
        :param subscription_id: ID of the subscription to get
        :param access_token: Access token for logged in user
        :return: Response
        """
        url = urlparse.urljoin(self.base_url, self.urls.me_subscription.format(subscription_id=subscription_id))

        params = {}
        body = {}

        headers = {
            'Accept': 'application/json'
        }

        if access_token:
            headers['Authorization'] = 'Bearer %s' % access_token

        response = requests.get(
            url,
            params=params,
            data=body,
            headers=headers
        )

        if response.status_code != 200:
            raise EcomResponseException(
                'Expected 200 response from GET /me/subscription/{subscription_id}, '
                'but received a %d response' % response.status_code,
                response
            )

        return response

    def update_me_subscription(
        self,
        access_token,
        subscription_id=None,
        payment_method_token=None,
        number_of_billing_cycles=None
    ):
        """
        /me/subscriptions/{subscription_id} (PUT)
        :param subscription_id: ID of the subscription to update
        :param payment_method_token: Token of the payment method to update
        :param number_of_billing_cycles: Number of billing cycles to update
        :param access_token: Access token for logged in user
        :return: Response
        """
        url = urlparse.urljoin(self.base_url, self.urls.me_subscription.format(subscription_id=subscription_id))

        params = {}
        body = {}

        headers = {
            'Accept': 'application/json'
        }

        if access_token:
            headers['Authorization'] = 'Bearer %s' % access_token

        if payment_method_token is not None:
            body['payment_method_token'] = payment_method_token
        if number_of_billing_cycles is not None:
            body['number_of_billing_cycle'] = number_of_billing_cycles

        response = requests.put(
            url,
            params=params,
            data=body,
            headers=headers
        )

        if response.status_code != 200:
            raise EcomResponseException(
                'Expected 200 response from PUT /me/subscriptions/{subscription_id}, '
                'but received a %d response' % response.status_code,
                response
            )

        return response

    def get_me_payment_method(self, access_token, payment_token=None):
        """
        /me/paymentmethods/{payment_token} (GET)
        :param payment_token: Token of the payment method to get
        :param access_token: Access token for logged in user
        :return: Response
        """
        url = urlparse.urljoin(self.base_url, self.urls.me_payment_method.format(payment_token=payment_token))

        params = {}
        body = {}

        headers = {
            'Accept': 'application/json'
        }

        if access_token:
            headers['Authorization'] = 'Bearer %s' % access_token

        response = requests.get(
            url,
            params=params,
            data=body,
            headers=headers
        )

        if response.status_code != 200:
            raise EcomResponseException(
                'Expected 200 response from GET /me/paymentmethods/{payment_token}, '
                'but received a %d response' % response.status_code,
                response
            )

        return response

    def update_me_payment_method(
            self,
            access_token,
            payment_token=None,
            nonce=None,
            device_data=None,
            billing_address_id=None
    ):
        """
        /me/paymentmethods/{payment_token} (PUT)
        :param payment_token: Token of the payment method to update
        :param nonce: Nonce of the new payment method
        :param device_data: Device data of the new payment method
        :param billing_address_id: Billing address Id of the new payment method
        :param access_token: Access token of the logged in user
        :return:
        """
        url = urlparse.urljoin(self.base_url, self.urls.me_payment_method.format(payment_token=payment_token))

        params = {}
        body = {}

        headers = {
            'Accept': 'application/json'
        }

        if access_token:
            headers['Authorization'] = 'Bearer %s' % access_token

        if nonce is not None:
            body['nonce'] = nonce
        if device_data is not None:
            body['device_data'] = device_data
        if billing_address_id is not None:
            body['billing_address_id'] = billing_address_id

        response = requests.put(
            url,
            params=params,
            data=body,
            headers=headers
        )

        if response.status_code != 200:
            raise EcomResponseException(
                'Expected 200 response from PUT /me/paymentmethods/{payment_token}, '
                'but received a %d response' % response.status_code,
                response
            )

        return response

    def get_me_orders(self, access_token, order_status=None):
        """
        /me/orders (GET)
        :param access_token: Access Token of the logged in user
        :param order_status: Status of orders to fetch (complete, pending_payment, cancel, fraud)
        :return: Response
        """
        url = urlparse.urljoin(self.base_url, self.urls.me_orders)

        params = {}
        body = {}

        if order_status:
            params['order_status'] = order_status

        headers = {
            'Accept': 'application/json'
        }

        if access_token:
            headers['Authorization'] = 'Bearer %s' % access_token

        response = requests.get(
            url,
            params=params,
            data=body,
            headers=headers
        )

        if response.status_code != 200:
            raise EcomResponseException(
                'Expected 200 response from GET /me/orders, but received a %d response' % response.status_code,
                response
            )

        return response

    def get_user_subscriptions(self, access_token, user_id=None):
        """
        /users/{user_id}/subscriptions (GET)
        :param user_id: User ID of the user to fetch subscriptions for
        :param access_token: Access Token of the logged in user
        :return: Response
        """
        url = urlparse.urljoin(self.base_url, self.urls.user_subscriptions.format(user_id=user_id))

        params = {}
        body = {}

        headers = {
            'Accept': 'application/json'
        }

        if access_token:
            headers['Authorization'] = 'Bearer %s' % access_token

        response = requests.get(
            url,
            params=params,
            data=body,
            headers=headers
        )

        if response.status_code != 200:
            raise EcomResponseException(
                'Expected 200 response from GET /users/{user_id}/subscriptions, '
                'but received a %d response' % response.status_code,
                response
            )

        return response

    def get_user_subscription(self, access_token, user_id=None, subscription_id=None):
        """
        /users/{user_id}/subscriptions/{subscription_id} (GET)
        :param user_id: User ID of user the subscription belongs to
        :param subscription_id: ID of the subscription to fetch
        :param access_token: Access Token of the logged in user
        :return: Response
        """
        url = urlparse.urljoin(
            self.base_url,
            self.urls.user_subscription.format(user_id=user_id,subscription_id=subscription_id)
        )

        params = {}
        body = {}

        headers = {
            'Accept': 'application/json'
        }

        if access_token:
            headers['Authorization'] = 'Bearer %s' % access_token

        response = requests.get(
            url,
            params=params,
            data=body,
            headers=headers
        )

        if response.status_code != 200:
            raise EcomResponseException(
                'Expected 200 response from GET /users/{user_id}/subscriptions/{subscription_id}, '
                'but received a %d response' % response.status_code,
                response
            )

        return response

    def update_user_subscription(
            self,
            access_token,
            user_id=None,
            subscription_id=None,
            payment_method_token=None,
            number_of_billing_cycles=None
    ):
        """
        /users/{user_id}/subscriptions/{subscription_id} (PUT)
        :param user_id: User ID of user the subscription belongs to
        :param subscription_id: ID of the subscription to update
        :param payment_method_token: Payment token of the payment method to update on the subscription
        :param number_of_billing_cycles: Number of billing cycles to update
        :param access_token: Access Token of the logged in user
        :return:
        """
        url = urlparse.urljoin(
            self.base_url,
            self.urls.user_subscription.format(user_id=user_id, subscription_id=subscription_id)
        )

        params = {}
        body = {}

        headers = {
            'Accept': 'application/json'
        }

        if access_token:
            headers['Authorization'] = 'Bearer %s' % access_token

        if payment_method_token is not None:
            body['payment_method_token'] = payment_method_token
        if number_of_billing_cycles is not None:
            body['number_of_billing_cycle'] = number_of_billing_cycles

        response = requests.put(
            url,
            params=params,
            data=body,
            headers=headers
        )

        if response.status_code != 200:
            raise EcomResponseException(
                'Expected 200 response from PUT /users/{user_id}/subscriptions/{subscription_id}, '
                'but received a %d response' % response.status_code,
                response
            )

        return response

    def get_user_payment_method(self, access_token, user_id=None, payment_token=None):
        """
        /users/{user_id}/paymentmethods/{payment_token} (GET)
        :param access_token: Access token of the logged in user
        :param user_id: User ID of the user to whom the payment token belongs
        :param payment_token: Payment token of the payment method to fetch
        :return:
        """
        url = urlparse.urljoin(
            self.base_url,
            self.urls.user_payment_method.format(user_id=user_id, payment_token=payment_token)
        )

        params = {}
        body = {}

        headers = {
            'Accept': 'application/json'
        }

        if access_token:
            headers['Authorization'] = 'Bearer %s' % access_token

        response = requests.get(
            url,
            params=params,
            data=body,
            headers=headers
        )

        if response.status_code != 200:
            raise EcomResponseException(
                'Expected 200 response from GET /users/{user_id}/paymentmethods/{payment_token}, '
                'but received a %d response' % response.status_code,
                response
            )

        return response

    def update_user_payment_method(
            self,
            access_token,
            user_id=None,
            payment_token=None,
            nonce=None,
            device_data=None,
            billing_address_id=None
    ):
        """
        /users/{user_id}/paymentmethods/{payment_token} (PUT)
        :param access_token: Access token of the logged in user
        :param user_id: ID of user to who the payment method belongs
        :param payment_token: Token of the payment method to update
        :param nonce: Nonce of the new payment method
        :param device_data: Device data of the new payment method
        :param billing_address_id: Billing address ID of the new payment method
        :return: Response
        """
        url = urlparse.urljoin(
            self.base_url,
            self.urls.user_payment_method.format(user_id=user_id, payment_token=payment_token)
        )

        params = {}
        body = {}

        headers = {
            'Accept': 'application/json'
        }

        if access_token:
            headers['Authorization'] = 'Bearer %s' % access_token

        if nonce:
            body['nonce'] = nonce

        if device_data:
            body['device_data'] = device_data

        if billing_address_id:
            body['billing_address_id'] = billing_address_id

        response = requests.put(
            url,
            params=params,
            data=body,
            headers=headers
        )

        if response.status_code != 200:
            raise EcomResponseException(
                'Expected 200 response from PUT /users/{user_id}/paymentmethods/{payment_token}, '
                'but received a %d response' % response.status_code,
                response
            )

        return response

    def get_user_orders(self, access_token, user_id=None, order_status=None):
        """
        /users/{user_id}/orders (GET)
        :param access_token: Access token of the logged in user
        :param user_id: ID of the user to fetch the orders for
        :param order_status: Status of orders to fetch (complete, pending_payment, cancel, fraud)
        :return: Response
        """
        url = urlparse.urljoin(self.base_url, self.urls.user_orders.format(user_id=user_id))

        params = {}
        body = {}

        if order_status:
            params['order_status'] = order_status

        headers = {
            'Accept': 'application/json'
        }

        if access_token:
            headers['Authorization'] = 'Bearer %s' % access_token

        response = requests.get(
            url,
            params=params,
            data=body,
            headers=headers
        )

        if response.status_code != 200:
            raise EcomResponseException(
                'Expected 200 response from GET /users/{user_id}/orders, '
                'but received a %d response' % response.status_code,
                response
            )

        return response

    def get_me_order(self, access_token, order_id=None):
        """
        /me/orders/{order_id} (GET)
        :param access_token: Access token of the logged in user
        :param order_id: ID of the order to fetch
        :return: Response
        """
        url = urlparse.urljoin(self.base_url, self.urls.me_order.format(order_id=order_id))

        params = {}
        body = {}

        headers = {
            'Accept': 'application/json'
        }

        if access_token:
            headers['Authorization'] = 'Bearer %s' % access_token

        response = requests.get(
            url,
            params=params,
            data=body,
            headers=headers
        )

        if response.status_code != 200:
            raise EcomResponseException(
                'Expected 200 response from GET /me/orders/{order_id}, '
                'but received a %d response' % response.status_code,
                response
            )

        return response

    def get_user_order(self, access_token, user_id=None, order_id=None):
        """
        /users/{user_id}/orders/{order_id} (GET)
        :param access_token: Access token of the logged in user
        :param user_id: ID of the user to whom the order belongs
        :param order_id: ID of the order to fetch
        :return: Response
        """
        url = urlparse.urljoin(self.base_url, self.urls.user_order.format(order_id=order_id, user_id=user_id))

        params = {}
        body = {}

        headers = {
            'Accept': 'application/json'
        }

        if access_token:
            headers['Authorization'] = 'Bearer %s' % access_token

        response = requests.get(
            url,
            params=params,
            data=body,
            headers=headers
        )

        if response.status_code != 200:
            raise EcomResponseException(
                'Expected 200 response from GET /users/{user_id}/orders/{order_id}, '
                'but received a %d response' % response.status_code,
                response
            )

        return response

    def get_me_invoice(self, access_token, order_id):
        """
        /me/orders/{order_id}/invoice (GET)
        :param access_token: Access token for logged in user
        :param order_id: ID of the order for which the invoice should be generated
        :return: Response
        """
        url = urlparse.urljoin(self.base_url, self.urls.me_invoice.format(order_id=order_id))

        headers = {
            'Accept': 'application/pdf'
        }

        if access_token:
            headers['Authorization'] = 'Bearer %s' % access_token

        response = requests.get(
            url,
            headers=headers
        )

        if response.status_code != 200:
            raise EcomResponseException(
                'Expected 200 response from GET /me/orders/{order_id}/invoice, but received a %d response' %
                response.status_code,
                response
            )

        return response

    def get_user_invoice(self, access_token, order_id, user_id):
        """
        /users/{user_id}/orders/{order_id}/invoice (GET)
        :param access_token: Access token for logged in user
        :param order_id: ID of the order for which the invoice should be generated
        :param user_id: User ID of the user to whom the order belongs
        :return: Response
        """
        url = urlparse.urljoin(self.base_url, self.urls.user_invoice.format(order_id=order_id, user_id=user_id))

        headers = {
            'Accept': 'application/pdf'
        }

        if access_token:
            headers['Authorization'] = 'Bearer %s' % access_token

        response = requests.get(
            url,
            headers=headers
        )

        if response.status_code != 200:
            raise EcomResponseException(
                'Expected 200 response from GET /users/{user_id}/orders/{order_id}/invoice, but received a %d response'
                % response.status_code,
                response
            )

        return response

    def add_me_plan_change_request(self, access_token, subscription_id=None, product_type_id=None):
        """
        /me/subscriptions/{subscription_id}/planchanges (POST)
        :param access_token: Access token for logged in user
        :param subscription_id: ID of the subscription to change plan for.
        :param product_type_id: product type ID of the new subscription plan
        :return: Response
        """
        url = urlparse.urljoin(
            self.base_url,
            self.urls.me_subscription_plan_change_request.format(subscription_id=subscription_id)
        )

        headers = {}

        body = {}

        if access_token:
            headers['Authorization'] = 'Bearer %s' % access_token

        if product_type_id:
            body['catalog_product_id'] = product_type_id

        response = requests.post(
            url,
            data=body,
            headers=headers
        )

        if response.status_code != 200:
            raise EcomResponseException(
                'Expected 200 response from POST /me/subscriptions/{subscription_id}/planchanges,' +
                'but received a %d response'
                % response.status_code,
                response
            )

        return response

    def add_user_plan_change_request(self, access_token, subscription_id=None, product_type_id=None, user_id=None):
        """
        /users/{user_id}/subscriptions/{subscription_id}/planchanges (POST)
        :param access_token: Access token for logged in user
        :param subscription_id: ID of the subscription to change plan for.
        :param product_type_id: product type ID of the new subscription plan
        :param user_id: User ID of the user to whom the subscription belongs
        :return: Response
        """
        url = urlparse.urljoin(
            self.base_url,
            self.urls.user_subscription_plan_change_request.format(subscription_id=subscription_id, user_id=user_id)
        )

        headers = {}

        body = {}

        if access_token:
            headers['Authorization'] = 'Bearer %s' % access_token

        if product_type_id:
            body['catalog_product_id'] = product_type_id

        response = requests.post(
            url,
            data=body,
            headers=headers
        )

        if response.status_code != 200:
            raise EcomResponseException(
                'Expected 200 response from POST /users/{user_id}/subscriptions/{subscription_id}/planchanges,' +
                'but received a %d response'
                % response.status_code,
                response
            )

        return response

    def update_me_plan_change_request(self, access_token, subscription_id=None, plan_change_id=None):
        """
        /me/subscriptions/{subscription_id}/planchanges/{plan_change_id} (PUT)
        :param access_token: Access token for logged in user
        :param subscription_id: ID of the subscription to change plan for.
        :param plan_change_id: Plan change request id to confirm.
        :return: Response
        """
        url = urlparse.urljoin(
            self.base_url,
            self.urls.me_subscription_plan_change_confirm.format(
                subscription_id=subscription_id,
                plan_change_id=plan_change_id
            )
        )

        headers = {}

        body = {}

        if access_token:
            headers['Authorization'] = 'Bearer %s' % access_token

        response = requests.put(
            url,
            data=body,
            headers=headers
        )

        if response.status_code != 200:
            raise EcomResponseException(
                'Expected 200 response from PUT /me/subscriptions/{subscription_id}/planchanges/{plan_change_id},' +
                'but received a %d response'
                % response.status_code,
                response
            )

        return response

    def update_user_plan_change_request(self, access_token, subscription_id=None, plan_change_id=None, user_id=None):
        """
        /users/{user_id}/subscriptions/{subscription_id}/planchanges/{plan_change_id} (PUT)
        :param access_token: Access token for logged in user
        :param subscription_id: ID of the subscription to change plan for.
        :param plan_change_id: Plan change request id to confirm.
        :param user_id: User ID of the user to whom the subscription belongs
        :return: Response
        """
        url = urlparse.urljoin(
            self.base_url,
            self.urls.user_subscription_plan_change_confirm.format(
                subscription_id=subscription_id,
                user_id=user_id,
                plan_change_id=plan_change_id
            )
        )

        headers = {}

        body = {}

        if access_token:
            headers['Authorization'] = 'Bearer %s' % access_token

        response = requests.put(
            url,
            data=body,
            headers=headers
        )

        if response.status_code != 200:
            raise EcomResponseException(
                'Expected 200 response from ' +
                'PUT /users/{user_id}/subscriptions/{subscription_id}/planchanges/{plan_change_id},' +
                'but received a %d response'
                % response.status_code,
                response
            )

        return response

    def create_or_get_order(self, user, access_token, create_order_for_user):
        """
        Get one of the default user's orders if possible, and if not, create a new one
        :param create_order_for_user: Function that creates an order for the given user (e.g. through Express Checkout)
        :param user: User object representing the user for which we want to create the order
        :param access_token: Access token for logged in user
        """
        all_orders = self.get_me_orders(access_token).json()['items']

        if all_orders:
            order = all_orders[0]
        else:
            create_order_for_user(user)
            order = self.get_me_orders(access_token).json()['items'][0]

        return order

    def create_or_get_subscription(self, user, access_token_profile, create_dj_suite_subscription_for_user):
        """
        Get one of the default user's subscriptions if possible, and if not, create a new one
        :param create_dj_suite_subscription_for_user: Function that creates a dj subscription for the given user
        :param user: User object representing the user for which we want to create the order
        :param access_token_profile: Access token for logged in user
        """
        subscriptions = self.get_me_subscriptions(access_token_profile).json()['items']

        if subscriptions:
            subscription = subscriptions[0]
        else:
            create_dj_suite_subscription_for_user(user)
            subscription = self.get_me_subscriptions(access_token_profile).json()['items'][0]

        return subscription

    def delete_me_subscription(
        self,
        access_token,
        subscription_id=None
    ):
        """
        /me/subscriptions/{subscription_id} (DELETE)
        :param subscription_id: ID of the subscription to delete
        :param access_token: Access token for logged in user
        :return: Response
        """
        url = urlparse.urljoin(self.base_url, self.urls.me_subscription.format(subscription_id=subscription_id))

        params = {}
        body = {}

        headers = {
            'Accept': 'application/json'
        }

        if access_token:
            headers['Authorization'] = 'Bearer %s' % access_token

        response = requests.delete(
            url,
            params=params,
            data=body,
            headers=headers
        )

        if response.status_code != 200:
            raise EcomResponseException(
                'Expected 200 response from DELETE /me/subscriptions/{subscription_id}, '
                'but received a %d response' % response.status_code,
                response
            )

        return response
    
    def delete_user_subscription(
        self,
        access_token,
        user_id=None,
        subscription_id=None
    ):
        """
        /users/{user_id}/subscriptions/{subscription_id} (DELETE)
        :param access_token: Access token of the logged in user
        :param user_id: user to whom the subscription belongs.
        :param subscription_id: ID of the subscription to delete
        :return:
        """
        url = urlparse.urljoin(self.base_url, self.urls.user_subscription.format(
            subscription_id=subscription_id,
            user_id=user_id
        ))

        params = {}
        body = {}

        headers = {
            'Accept': 'application/json'
        }

        if access_token:
            headers['Authorization'] = 'Bearer %s' % access_token

        response = requests.delete(
            url,
            params=params,
            data=body,
            headers=headers
        )

        if response.status_code != 200:
            raise EcomResponseException(
                'Expected 200 response from DELETE /users/{user_id}/subscriptions/{subscription_id}, '
                'but received a %d response' % response.status_code,
                response
            )

        return response


class EcomException(Exception):
    """
    Generic error thrown when unexpected results are received from the Ecom service
    """
    pass


class EcomResponseException(ResponseException):
    """
    Thrown when an error response is received from the Ecom service
    """
    pass
