""" Model classes for use in tests, primarily to make the code easier to read/understand, and to make comparisons
  between objects simpler. """
from datetime import datetime


class Model(object):

    def matches(self, other, attrs_to_match=None):
        """
        :param other: Object to compare this one with
        :param attrs_to_match: List of attributes to match against
        :return: True if the two objects match
        """
        attr_list = attrs_to_match or self.default_comparison_attrs
        return self.compare_attrs(other, attr_list)

    @property
    def default_comparison_attrs(self):
        """
        :return: List of attributes to match in a comparison (e.g. enough to uniquely identify this object)
        """
        raise NotImplementedError

    def compare_attrs(self, other, attrs):
        """
        Compares the attributes in the `attrs` list for the two objects (self and other), returning true if they are
        identical.
        TODO Use dictionary comprehension syntax if we upgrade to Python 3
        """
        this_dict = dict([(k, v) for k, v in self.__dict__.items() if k in attrs])
        other_dict = dict([(k, v) for k, v in other.__dict__.items() if k in attrs])
        return this_dict == other_dict


class User(Model):

    # Attributes used to uniquely identify the user
    default_comparison_attrs = ['id', 'email']

    def __init__(self, user_id, email, password=None, first_name=None, last_name=None, date_created=None, locale=None):
        self.id = user_id
        self.email = email
        self.password = password
        self.first_name = first_name or None
        self.last_name = last_name or None
        self.date_created = date_created or None
        self.locale = locale or None

    def matches(self, user_data, attrs_to_match=None):
        """
        Checks whether the given user_data dictionary / response body has data that identifies it as the same user as
        this one.
        """
        other_user = User.load_from(user_data)
        return super(User, self).matches(other_user, attrs_to_match)

    @staticmethod
    def data_matches(this_user_data, other_user_data, attrs_to_match=None):
        """
        Checks whether two dictionaries of user data refer to the same user.
        """
        this_user = User.load_from(this_user_data)
        other_user = User.load_from(other_user_data)
        return super(User, this_user).matches(other_user, attrs_to_match)

    @staticmethod
    def load_from(user_data):
        """
        Creates a User object from a response body / dictionary of user data
        """
        data = dict(user_data)
        data['email'] = data.pop('email_address', None) or data.get('email', None)
        data['user_id'] = data.pop('id', None) or data.get('user_id', None)
        data['date_created'] = data.pop('timestamp', None) or data.get('date_created', None)
        return User(**data)


class Address(Model):

    default_comparison_attrs = ['address_one', 'address_two', 'city', 'post_code', 'country']

    def __init__(self, address_one=None, address_two=None, city=None, post_code=None, country=None):
        self.address_one = address_one or '4 Test Drive'
        self.address_two = address_two or 'Testville'
        self.city = city or 'Testerton'
        self.post_code = post_code or '0101'
        self.country_code = country or 'NZ'


class CreditCard(Model):

    default_comparison_attrs = ['card_number', 'expiration_date', 'cvv']

    def __init__(self, card_number=None, expiration_date=None, cvv=None):
        self.card_number = card_number or '4111111111111111'
        self.expiration_date = expiration_date or datetime(2025, 10, 25)
        self.cvv = cvv or 999

    @property
    def formatted_expiration_date(self):
        if not self.expiration_date:
            return ''
        else:
            return self.expiration_date.strftime('%m/%y')


class Coupon(Model):

    default_comparison_attrs = ['coupon_code']

    def __init__(self, coupon_code=None):
        self.coupon_code = coupon_code or '25OFFEXPPACKS'
