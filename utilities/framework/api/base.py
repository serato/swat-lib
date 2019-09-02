import functools
from types import FunctionType


def log_request_and_response(func):
    """
    Decorator that logs the responses (and the requests they are responses to) returned by any given 'func'. Useful if
    you want to log all the responses returned to / requests made by an API wrapper.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        response = None
        try:
            response = func(*args, **kwargs)
        except ResponseException as e:
            response = e.response  # Got a non-20x response
            raise  # May need to change this to preserve the original traceback in Python 3
        finally:
            # We still want to log the request/response if we receive an IdResponseException (i.e. and error response)
            if response is not None:  # Note: failure responses are falsey!
                # Attempt to find a logger, and log the request and response
                logger = getattr(args[0], 'logger', None)
                if logger:  # Only exists if the calling class has a logger attribute
                    logger.info(logger.format.format_request(response.request))
                    logger.info(logger.format.format_response(response))
        return response

    return wrapper


class MetaApi(type):
    """
    Metaclass for API wrapper classes that allows all requests/responses to be pretty-printed and logged (at 'info'
    logging level and above).
    """

    def __new__(mcs, class_name, bases, class_dict):
        new_class_dict = {}
        ancestor = MetaApi.get_furthest_ancestor(bases[0])

        for attribute_name, attribute in class_dict.items():
            # Log the pretty-printed request and response, if this method represents an API call
            if not attribute_name.startswith('__') and isinstance(attribute, FunctionType):
                if hasattr(ancestor, attribute_name):  # I.e. this method overrides a method in the furthest ancestor
                    attribute = log_request_and_response(attribute)
            new_class_dict[attribute_name] = attribute
        return type.__new__(mcs, class_name, bases, new_class_dict)

    @classmethod
    def get_furthest_ancestor(mcs, base):
        """
        Gets the first class in an inheritance hierarchy that has this class as its metaclass.
        """
        ancestor = base

        while getattr(base.__base__, '__metaclass__', None) == mcs:
            ancestor = base.__base__

        return ancestor


class ResponseException(Exception):
    """
    Thrown when an error response is received from an API.
    """
    def __init__(self, message, response):
        """
        :param message: Message for the exception
        :param response HTTP response object
        """
        super(Exception, self).__init__(message)
        self.status_code = response.status_code
        self.error_code = int(response.headers.get('X-Serato-ErrorCode') or 0)
        self.response = response
