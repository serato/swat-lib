import functools

from bs4 import BeautifulSoup


def try_soup(func, bs_func_name):
    def wrapper(*args):
        if args[0].soup:
            soup_func = getattr(args[0].soup, bs_func_name)
            return soup_func(func(*args))
        else:
            raise NoSoupException
    return wrapper


def find_all(func):
    """
    Decorator that wraps the return value of a function call with BeautifulSoup::find_all()
    """
    return try_soup(func, 'find_all')


class MetaEmail(type):
    """
    MetaClass for wrapping calling BeautifulSoup function on property values. Extension for the future: some way of
    flagging a property to be wrapped in BeautifulSoup::find(), instead of find_all() (check for plurals?)
    """
    def __new__(mcs, class_name, bases, class_dict):
        new_class_dict = {}

        for attribute_name, attribute in class_dict.items():
            new_attr = attribute
            if isinstance(attribute, property):
                # Wrap all properties in BeautifulSoup's find_all()
                new_attr = property(find_all(attribute.__get__), attribute.__set__,  attribute.__delattr__)
            new_class_dict[attribute_name] = new_attr

        return type.__new__(mcs, class_name, bases, new_class_dict)


class BaseEmail(object):
    """
    Utility class for parsing HTML emails. The value of any property defined on a class that extends this will be
    treated as an argument for BeautifulSoup's find_all(), the return value of which will replace that property's value.
    Generally convenient, but use at your own risk.
    """
    __metaclass__ = MetaEmail

    def __init__(self, html):
        self.soup = BeautifulSoup(html, 'html.parser')


class NoSoupException(Exception):
    def __init__(self):
        super(NoSoupException, self).__init__('self.soup is not defined! It should be a BeautifulSoup instance.')
